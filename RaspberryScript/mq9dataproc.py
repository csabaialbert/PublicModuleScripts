import time
import math
import serial

# A programkód alapja George Soloupis által készült.
# Az eredeti kód elérhető: https://github.com/farmaker47/Raspberry-to-assess-food-quality/tree/main/code 

class MQ9dataproc():

    rawDataValue = 99999.00

    ######################### Hardware Related Macros #########################
    RL_VALUE                     = 10       # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 9.83     # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from the chart in datasheet
 
    ######################### Software Related Macros #########################
    CALIBRATION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 50       # define the time interval(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define the time interval(in milisecond) between each samples in
    READ_SAMPLE_TIMES            = 5        # define how many samples you are going to take in normal operation 
                                            # normal operation
 
    ######################### Application Related Macros ######################
    GAS_CO                       = 0
    GAS_LPG                      = 1
    GAS_CH4                      = 2

    # Az adatok a soros csatornán érkeznek az Arduino felől.
    # Soros kapcsolat inicializálása és a puffer ürítése. 

    seri = serial.Serial('/dev/ttyUSB0', 9600)
    seri.reset_input_buffer()


    def __init__(self, Ro=10):

        # soros csatorna olvasása, amíg az adott sor nem felel meg.
        while(self.rawDataValue == 99999.00):
            serialText = str(self.seri.readline())
            strippedText = serialText[2:-5]
            print(strippedText)
            if(strippedText.startswith("MQ9:")):
                mq9Value = strippedText.split(':')[1][1:-1]
                self.rawDataValue = float(mq9Value)
        
        self.Ro = Ro 
        
        self.COCurve = [2.3,0.24,-0.49]     # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent"
                                            # to the original curve. 
                                            # data format:{ x, y, slope}; point1: (lg200, 0.24), point2: (lg1000, -0.10) 
        self.LPGCurve =[2.3,0.32,-0.47]     # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg200, 0.32), point2: (lg10000, -0.48)
        self.CH4Curve =[2.3,0.49,-0.38]     # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg200, 0.49), point2: (lg10000,  -0.15)
                
        print("Calibrating MQ-9...")
        self.Ro = self.MQ9_Calibration()
        print("Calibration of MQ-9 is done...")
        print("MQ-9 Ro=%f kohm" % self.Ro)
        print("\n")
    
    ######################### MQCalibration ####################################
    # Input:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          MQResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
    #          9.83, which differs slightly between different sensors.
    ############################################################################ 

    ## Szenzor kalibrálása.
    def MQ9_Calibration(self):
        val = 0.0
        for i in range(self.CALIBRATION_SAMPLE_TIMES):          # take multiple samples
            needToRead = True
            while(needToRead):
                ##adatok olvasása a soros csatornáról, amíg nem kerül kiolvasásra elegendő adat az előírt kalibrálás elvégzéséhez.
                serialText = str(self.seri.readline())
                strippedText = serialText[2:-5]
                if(strippedText.startswith("MQ9:")):
                    mq9Value = strippedText.split(':')[1][1:-1]
                    self.rawDataValue = float(mq9Value)
                    needToRead = False
            val += self.MQResistanceCalculation(self.rawDataValue)
            needToRead = True
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            
        val = val/self.CALIBRATION_SAMPLE_TIMES                 # calculate the average value
        val = val/self.RO_CLEAN_AIR_FACTOR                      # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                # according to the chart in the datasheet 
        return val
        
    ######################### MQResistanceCalculation #########################
    # Input:   raw_adc - raw value read from adc, which represents the voltage
    # Output:  the calculated sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 

    ##Szenzor ellenállásának meghatározása a kiolvasott értékből.
    def MQResistanceCalculation(self, raw_adc):
        #print(raw_adc)
        # 1023 for 3008()
        # https://github.com/tutRPi/Raspberry-Pi-Gas-Sensor-MQ
        
        # 65472 for circuit python
        # Even though the MCP3008 is a 10-bit ADC, the value returned is a 16-bit number to provide a consistent interface across ADCs in CircuitPython
        # https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/blob/main/adafruit_mcp3xxx/analog_in.py#L50-L54
        
        if raw_adc == 0:
            raw_adc = 1
            
        return float(self.RL_VALUE * (1023.0-raw_adc) / float(raw_adc))    
      
    #########################  MQRead ##########################################
    # Input:   mq_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target
    #          gas. The sample times and the time interval between samples could be configured
    #          by changing the definition of the macros.
    ############################################################################ ,

    ## Adatokat kiolvasó függvény.
    def MQRead(self):
        rs = 0.0
        raw_value = 0.0
        needToRead = True
        for i in range(self.READ_SAMPLE_TIMES):
            while(needToRead):
                ## Adatok olvasása, amíg nem kerül kiolvasásra elegendő. (fent megadott 5 db)
                serialText = str(self.seri.readline())
                strippedText = serialText[2:-5]
                if(strippedText.startswith("MQ9:")):
                    mq9Value = strippedText.split(':')[1][1:-1]
                    self.rawDataValue = float(mq9Value)
                    needToRead = False
            raw_value += self.rawDataValue
            rs += self.MQResistanceCalculation(self.rawDataValue)
            needToRead = True
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)

        rs = rs / self.READ_SAMPLE_TIMES
        raw_value = raw_value / self.READ_SAMPLE_TIMES

        return rs, raw_value
    
    ## Számolt értékeket visszaadó függvény.
    def MQPercentage(self):
        val = {}
        read, raw_value = self.MQRead()
        val["CO"]       = self.MQGetGasPercentage(read/self.Ro, self.GAS_CO)
        val["LPG"]      = self.MQGetGasPercentage(read/self.Ro, self.GAS_LPG)
        val["CH4"]      = self.MQGetGasPercentage(read/self.Ro, self.GAS_CH4)
        val["RAW_VALUE"]= raw_value
        return val
     
    #########################  MQGetGasPercentage ##############################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function passes different curves to the MQGetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 

    ## Adott gáz koncentrációjának értékét kiszámító függvényt meghívó függvény.
    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        if ( gas_id == self.GAS_CO ):
            return self.MQGetPercentage(rs_ro_ratio, self.COCurve)
        elif ( gas_id == self.GAS_LPG ):
            return self.MQGetPercentage(rs_ro_ratio, self.LPGCurve)
        elif ( gas_id == self.GAS_CH4 ):
            return self.MQGetPercentage(rs_ro_ratio, self.CH4Curve)
        return 0
     
    #########################  MQGetPercentage #################################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
    #          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
    #          value.
    ############################################################################ 

    ##Értékeket meghatározó függvény.
    def MQGetPercentage(self, rs_ro_ratio, pcurve):
        #print(rs_ro_ratio)
        #print((math.log(rs_ro_ratio)-pcurve[1]))
        #print(((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0]))
        
        # This is the natural natural logarithm -> log(rs_ro_ratio)
        return (math.pow(10,(((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0])))

