#include <Adafruit_AHTX0.h>
#include <MCP3008.h>

#define CS_PIN 12
#define CLOCK_PIN 9
#define MOSI_PIN 11
#define MISO_PIN 10


Adafruit_AHTX0 aht;

MCP3008 adc(CLOCK_PIN,MOSI_PIN,MISO_PIN,CS_PIN);  

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

   if(!aht.begin())
   {
      Serial.println("Could not find AHT...");
   }
   Serial.println("AHT10 found!");
}

void loop() {
  // put your main code here, to run repeatedly:

  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);
  
  int val = adc.readADC(0);
  char sval[50];
  ltoa(val, sval, 10);
  Serial.print("MQ2:");
  Serial.println(String("") + "{" + val + "}");
  
  int val1 = adc.readADC(1);
  char sval1[50];
  ltoa(val1, sval1, 10);
  Serial.print("MQ3:");
  Serial.println(String("") + "{" + val1 + "}");

  int val2 = adc.readADC(2);
  char sval2[50];
  ltoa(val2, sval2, 10);
  Serial.print("MQ4:");
  Serial.println(String("") + "{" + val2 + "}");

  int val3 = adc.readADC(3);
  char sval3[50];
  ltoa(val3, sval3, 10);
  Serial.print("MQ135:");
  Serial.println(String("") + "{" + val3 + "}");
  
  int val4 = adc.readADC(4);
  char sval4[50];
  ltoa(val4, sval4, 10);
  Serial.print("MQ6:");
  Serial.println(String("") + "{" + val4 +"}");
  
  int val5 = adc.readADC(5);
  char sval5[50];
  ltoa(val5, sval5, 10);
  Serial.print("MQ7:");
  Serial.println(String("") + "{" + val5 + "}");

  int val6 = adc.readADC(6);
  char sval6[50];
  ltoa(val6, sval6, 10);
  Serial.print("MQ8:");
  Serial.println(String("") + "{" + val6 + "}");
  
  int val7 = adc.readADC(7);
  char sval7[50];
  ltoa(val7, sval7, 10);
  Serial.print("MQ9:");
  Serial.println(String("") + "{" + val7 + "}");
 
  
  Serial.println(String("") + "Humidity:" + "{" + humidity.relative_humidity + "}");
  Serial.println(String("") + "Temperature:" + "{" + temp.temperature + "}");

  char shumidity[50];
  ltoa(humidity.relative_humidity, shumidity, 10);

  char stemp[50];
  ltoa(temp.temperature, stemp, 10);
  
  Serial.println("+++++++++++++++++++++");
  
  String serialString =  String(sval) + ";" + String(sval1) + ";" + String(sval2) + ";" + String(sval3) + ";" + String(sval4) + ";" + String(sval5) + ";" + String(sval6) + ";" + String(sval7) + ";" + String(shumidity) + ";" + String(stemp);
  int str_len = serialString.length() + 1;
  char serialArray[str_len];
  serialString.toCharArray(serialArray, str_len);
  delay(50);
  
}
