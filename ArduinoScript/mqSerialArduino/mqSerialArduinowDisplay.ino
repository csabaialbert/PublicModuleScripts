//felhasználásra kerülő könyvtárak
#include <Adafruit_AHTX0.h>
#include <MCP3008.h>
#include <LiquidCrystal_I2C.h>

//MCP3008 AD konverter csatlakozási pin-jeinek megadása 
#define CS_PIN 12
#define CLOCK_PIN 9
#define MOSI_PIN 11
#define MISO_PIN 10

int counter=99;

//kijelző csatlakoztatási adatainak megadása
LiquidCrystal_I2C lcd(0x27, 16, 2);
//AHT10 szenzor inicializálása
Adafruit_AHTX0 aht;

//AD konverter inicializálása
MCP3008 adc(CLOCK_PIN,MOSI_PIN,MISO_PIN,CS_PIN);  


void setup() {
  //soros kapcsolat megkezdése
  Serial.begin(9600);
  //kijelző inicializálása, és a háttérvilágjtásának bekapcsolása
  lcd.init();
  lcd.backlight();
  
  //AHT szenzor kapcsolatának indítása.
   if(!aht.begin())
   {
      Serial.println("Could not find AHT...");
   }
   Serial.println("AHT10 found!");
}

void loop() {
 
  //hőmérséklet és páratartalom értékek kiolvasása.
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);
  
  //AD koverter 0. csatornájára kötött (MQ-2) szenzor értékének kiolvasása.
  int val = adc.readADC(0);
  //Kiolvasott érték kiírása soros portra.
  Serial.print("MQ2:");
  Serial.println(String("") + "{" + val + "}");
  
  int val1 = adc.readADC(1);
  Serial.print("MQ3:");
  Serial.println(String("") + "{" + val1 + "}");

  int val2 = adc.readADC(2);
  Serial.print("MQ4:");
  Serial.println(String("") + "{" + val2 + "}");

  int val3 = adc.readADC(3);
  Serial.print("MQ135:");
  Serial.println(String("") + "{" + val3 + "}");
  
  int val4 = adc.readADC(4);
  Serial.print("MQ6:");
  Serial.println(String("") + "{" + val4 +"}");
  
  int val5 = adc.readADC(5);
  Serial.print("MQ7:");
  Serial.println(String("") + "{" + val5 + "}");

  int val6 = adc.readADC(6);
  Serial.print("MQ8:");
  Serial.println(String("") + "{" + val6 + "}");
  
  int val7 = adc.readADC(7);
  Serial.print("MQ9:");
  Serial.println(String("") + "{" + val7 + "}");

  //hőmérséklet és páratartalom értékek kiíratása soros portra.
  Serial.println(String("") + "Humidity:" + "{" + humidity.relative_humidity + "}");
  Serial.println(String("") + "Temperature:" + "{" + temp.temperature + "}");
  
  if(counter > 100)
  {
    //Minden századik ciklusban frissítésre kerülnek a kiírt hőmérséklet és páratartalom adatok.
    lcd.setCursor(0, 0);
    lcd.print(String("") + "Hum:"+ humidity.relative_humidity+" %");
    lcd.setCursor(0, 1);
    lcd.print(String("") + "Temp:"+ temp.temperature + "Cels.");
    counter = 0;
  }
  counter = counter + 1;
  //50 ms késleltetés.
  delay(50);
  
}
