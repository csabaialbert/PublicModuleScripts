#!usr/bin/env python3
import serial
import random
import mq2dataproc
import mq3dataproc
import mq4dataproc
import mq135dataproc
import mq6dataproc
import mq7dataproc
import mq8dataproc
import mq9dataproc
import sys, time



mq2Value = ""
mq3Value = ""
mq4Value = ""
mq135Value = ""
mq6Value = ""
mq7Value = ""
mq8Value = ""
mq9Value = ""
tempValue = ""
humidityValue = ""
mq2 = mq2dataproc.MQ2dataproc()
mq3 = mq3dataproc.MQ3dataproc()
mq4 = mq4dataproc.MQ4dataproc()
mq135 = mq135dataproc.MQ135dataproc()
mq6 = mq6dataproc.MQ6dataproc()
mq7 = mq7dataproc.MQ7dataproc()
mq8 = mq8dataproc.MQ8dataproc()
mq9 = mq9dataproc.MQ9dataproc()


if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	ser.reset_input_buffer()
	
	counter = 0
	while True:
		serialText = str(ser.readline())
		strippedText = serialText[2:-5]
		
		if strippedText.startswith("MQ2:"):
			mq2Value = strippedText.split(':')[1][1:-1]
			mq2dataproc.rawDataValue = float(mq2Value)
			percentmq2 = mq2.MQPercentage()
			print("MQ2 measurment")
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("Raw_value:   %g, \nLPG:         %.5f ppm, \nCO:          %.5f ppm, \nSmoke:       %.5f ppm, \nPropane:     %.5f ppm, \nH2:          %.5f ppm, \nAlcohol:     %.5f ppm, \nCH4:         %.5f ppm" % (percentmq2["RAW_VALUE"], percentmq2["GAS_LPG"], percentmq2["CO"], percentmq2["SMOKE"], percentmq2["PROPANE"], percentmq2["H2"], percentmq2["ALCOHOL"], percentmq2["CH4"]))
			sys.stdout.flush()
			print("\n\n")
			
		elif strippedText.startswith("MQ3:"):
			mq3Value = strippedText.split(':')[1][1:-1]
			mq3dataproc.rawDataValue = float(mq3Value)
			percentmq3 = mq3.MQPercentage()
			print("MQ3 measurment")
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("Raw_value:   %g, \nAlcohol:     %.5f mg/L, \nBenzine:     %.5f mg/L, \nExane:       %.5f mg/L, \nLPG:         %.5f mg/L, \nCO:          %.5f mg/L, \nCH4:         %.5f mg/L" % (percentmq3["RAW_VALUE"], percentmq3["ALCOHOL"], percentmq3["BENZINE"], percentmq3["EXANE"], percentmq3["LPG"], percentmq3["CO"], percentmq3["CH4"]))
			sys.stdout.flush()
			print("\n\n")
		
		elif strippedText.startswith("MQ4:"):
			mq4Value = strippedText.split(':')[1][1:-1]
			mq4dataproc.rawDataValue = float(mq4Value)
			percentmq4 = mq4.MQPercentage()
			print("MQ4 measurment")
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("Raw_value:   %g, \nCH4:         %.5f ppm, \nLPG:         %.5f ppm, \nH2:          %.5f ppm, \nSmoke:       %.5f ppm, \nAlcohol:     %.5f ppm, \nCO:          %.5f ppm" % (percentmq4["RAW_VALUE"], percentmq4["CH4"], percentmq4["LPG"], percentmq4["H2"], percentmq4["SMOKE"], percentmq4["ALCOHOL"], percentmq4["CO"]))
			sys.stdout.flush()
			print("\n\n")
		
		elif strippedText.startswith("MQ135:"):
			mq135Value = strippedText.split(':')[1][1:-1]
			mq135dataproc.rawDataValue = float(mq135Value)
			percentmq135 = mq135.MQPercentage()
			print("MQ135 measurment")
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("Raw_value:   %g, \nACETON:      %.5f ppm, \nTOLUENO:     %.5f ppm, \nALCOHOL:     %.5f ppm, \nCO2:         %.5f ppm, \nNH4:         %.5f ppm, \nCO:          %.5f ppm" % (percentmq135["RAW_VALUE"], percentmq135["ACETON"], percentmq135["TOLUENO"], percentmq135["ALCOHOL"], percentmq135["CO2"], percentmq135["NH4"], percentmq135["CO"]))
			sys.stdout.flush()
			print("\n\n")
		
		elif strippedText.startswith("MQ6:"):
			mq6Value = strippedText.split(':')[1][1:-1]
			mq6dataproc.rawDataValue = float(mq6Value)
			percentmq6 = mq6.MQPercentage()
			print("MQ6 measurment")
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("Raw_value:   %g, \nLPG:         %.5f ppm, \nCH4:         %.5f ppm, \nH2:          %.5f ppm, \nAlcohol:     %.5f ppm, \nCO:          %.5f ppm" % (percentmq6["RAW_VALUE"], percentmq6["LPG"], percentmq6["CH4"], percentmq6["H2"], percentmq6["ALCOHOL"], percentmq6["CO"]))
			sys.stdout.flush()
			print("\n\n")
		
		elif strippedText.startswith("MQ7:"):
			mq7Value = strippedText.split(':')[1][1:-1]
			mq7dataproc.rawDataValue = float(mq7Value)
			percentmq7 = mq7.MQPercentage()
			print("MQ7 measurment")
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("Raw_value:   %g, \nH2:          %.5f ppm, \nCO:          %.5f ppm, \nLPG:         %.5f ppm, \nCH4:         %.5f ppm, \nAlcohol:     %.5f ppm" % (percentmq7["RAW_VALUE"], percentmq7["H2"], percentmq7["CO"], percentmq7["LPG"], percentmq7["CH4"], percentmq7["ALCOHOL"]))
			sys.stdout.flush()
			print("\n\n")
		
		elif strippedText.startswith("MQ8:"):
			mq8Value = strippedText.split(':')[1][1:-1]
			mq8dataproc.rawDataValue = float(mq8Value)
			percentmq8 = mq8.MQPercentage()
			print("MQ8 measurment")
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("Raw_value:   %g, \nH2:          %.5f ppm, \nAlcohol:     %.5f ppm, \nLPG:         %.5f ppm, \nCH4:         %.5f ppm, \nCO:          %.5f ppm" % (percentmq8["RAW_VALUE"], percentmq8["H2"], percentmq8["ALCOHOL"], percentmq8["LPG"], percentmq8["CH4"], percentmq8["CO"]))
			sys.stdout.flush()
			print("\n\n")
		
		elif strippedText.startswith("MQ9:"):
			mq9Value = strippedText.split(':')[1][1:-1]
			mq9dataproc.rawDataValue = float(mq9Value)
			percentmq9 = mq9.MQPercentage()
			print("MQ9 measurment")
			sys.stdout.write("\r")
			sys.stdout.write("\033[K")
			sys.stdout.write("Raw_value:   %g, \nCO:          %.5f ppm, \nLPG:         %.5f ppm, \nCH4:         %.5f ppm" % (percentmq9["RAW_VALUE"], percentmq9["CO"], percentmq9["LPG"], percentmq9["CH4"]))
			sys.stdout.flush()
			print("\n\n")
		
		elif strippedText.startswith("Temperature:"):
			tempValue = strippedText.split(':')[1][1:-1]
			print("Temperature: " + tempValue + "°C")
			print("\n\n")
		
		elif strippedText.startswith("Humidity:"):
			humidityValue = strippedText.split(':')[1][1:-1]
			print("Humidity: " + humidityValue + "%")
			print("\n\n")
			
		if ( counter == 10):
			print("Sleep for 30 sec..\n\n")
			counter = 0
			time.sleep(10)
		else:
			counter = counter + 1
		

