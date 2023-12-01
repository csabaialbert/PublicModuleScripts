#!usr/bin/env python3

# Könyvtárak importálása
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
import requests
import jwt
import json

#Globális változók deklarálása
token=""
moduleId = "1"
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
dataToSend = {}

#Szenzorok inicializálása az adatfeldolgozó scriptekkel.
mq2 = mq2dataproc.MQ2dataproc()
mq3 = mq3dataproc.MQ3dataproc()
mq4 = mq4dataproc.MQ4dataproc()
mq135 = mq135dataproc.MQ135dataproc()
mq6 = mq6dataproc.MQ6dataproc()
mq7 = mq7dataproc.MQ7dataproc()
mq8 = mq8dataproc.MQ8dataproc()
mq9 = mq9dataproc.MQ9dataproc()



if __name__ == '__main__':
	#Indításkor lefutó programrész.
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	ser.reset_input_buffer()
	r = requests.post('https://xxxxx', json={"xxxxx"})		
	resp= r.json()
	token=resp["token"]
	print(resp["token"])
	counter = 0

	#Ismétlődően lefutó programrész.
	while True:
		#Soros csatornán lévő adatok kiolvasása.
		serialText = str(ser.readline())
		#Kiolvasott szöveg elejéről levágásra kerülnek a felesleges karakterek.
		strippedText = serialText[2:-5]
		
		#Ellenőrzésre kerül, hogy at adott sor melyik szenzorhoz tartozó értékeket tartalmazza.
		if strippedText.startswith("MQ2:"):
			#adatok kinyerése a szövegből.
			mq2Value = strippedText.split(':')[1][1:-1]
			mq2dataproc.rawDataValue = float(mq2Value)
			percentmq2 = mq2.MQPercentage()
			
		elif strippedText.startswith("MQ3:"):
			mq3Value = strippedText.split(':')[1][1:-1]
			mq3dataproc.rawDataValue = float(mq3Value)
			percentmq3 = mq3.MQPercentage()
		
		elif strippedText.startswith("MQ4:"):
			mq4Value = strippedText.split(':')[1][1:-1]
			mq4dataproc.rawDataValue = float(mq4Value)
			percentmq4 = mq4.MQPercentage()
		
		elif strippedText.startswith("MQ135:"):
			mq135Value = strippedText.split(':')[1][1:-1]
			mq135dataproc.rawDataValue = float(mq135Value)
			percentmq135 = mq135.MQPercentage()
		
		elif strippedText.startswith("MQ6:"):
			mq6Value = strippedText.split(':')[1][1:-1]
			mq6dataproc.rawDataValue = float(mq6Value)
			percentmq6 = mq6.MQPercentage()
		
		elif strippedText.startswith("MQ7:"):
			mq7Value = strippedText.split(':')[1][1:-1]
			mq7dataproc.rawDataValue = float(mq7Value)
			percentmq7 = mq7.MQPercentage()
		
		elif strippedText.startswith("MQ8:"):
			mq8Value = strippedText.split(':')[1][1:-1]
			mq8dataproc.rawDataValue = float(mq8Value)
			percentmq8 = mq8.MQPercentage()
		
		elif strippedText.startswith("MQ9:"):
			mq9Value = strippedText.split(':')[1][1:-1]
			mq9dataproc.rawDataValue = float(mq9Value)
			percentmq9 = mq9.MQPercentage()
		
		elif strippedText.startswith("Temperature:"):
			tempValue = strippedText.split(':')[1][1:-1]
		
		elif strippedText.startswith("Humidity:"):
			humidityValue = strippedText.split(':')[1][1:-1]
		#Kiolvasott adatok szótárba való rendezése	
		try:	
			dataToSend["mq2Raw"]=str("{:.4f}".format(percentmq2["RAW_VALUE"]))
			dataToSend["mq2Lpg"]=str("{:.4f}".format(percentmq2["GAS_LPG"]))
			dataToSend["mq2Co"]=str("{:.4f}".format(percentmq2["CO"]))
			dataToSend["mq2Smoke"]=str("{:.4f}".format(percentmq2["SMOKE"]))
			dataToSend["mq2Propane"]=str("{:.4f}".format(percentmq2["PROPANE"]))
			dataToSend["mq2H2"]=str("{:.4f}".format(percentmq2["H2"]))
			dataToSend["mq2Alcohol"]=str("{:.4f}".format(percentmq2["ALCOHOL"]))
			dataToSend["mq2Ch4"]=str("{:.4f}".format(percentmq2["CH4"]))

			dataToSend["mq3Raw"]=str("{:.4f}".format(percentmq3["RAW_VALUE"]))
			dataToSend["mq3Alcohol"]=str("{:.4f}".format(percentmq3["ALCOHOL"]))
			dataToSend["mq3Benzine"]=str("{:.4f}".format(percentmq3["BENZINE"]))
			dataToSend["mq3Exane"]=str("{:.4f}".format(percentmq3["EXANE"]))
			dataToSend["mq3Lpg"]=str("{:.4f}".format(percentmq3["LPG"]))
			dataToSend["mq3Co"]=str("{:.4f}".format(percentmq3["CO"]))
			dataToSend["mq3Ch4"]=str("{:.4f}".format(percentmq3["CH4"]))

			dataToSend["mq4Raw"]=str("{:.4f}".format(percentmq4["RAW_VALUE"]))
			dataToSend["mq4Ch4"]=str("{:.4f}".format(percentmq4["CH4"]))
			dataToSend["mq4Lpg"]=str("{:.4f}".format(percentmq4["LPG"]))
			dataToSend["mq4H2"]=str("{:.4f}".format(percentmq4["H2"]))
			dataToSend["mq4Smoke"]=str("{:.4f}".format(percentmq4["SMOKE"]))
			dataToSend["mq4Alcohol"]=str("{:.4f}".format(percentmq4["ALCOHOL"]))
			dataToSend["mq4Co"]=str("{:.4f}".format(percentmq4["CO"]))

			dataToSend["mq135Raw"]=str("{:.4f}".format(percentmq135["RAW_VALUE"]))
			dataToSend["mq135Aceton"]=str("{:.4f}".format(percentmq135["ACETON"]))	
			dataToSend["mq135Tolueno"]=str("{:.4f}".format(percentmq135["TOLUENO"]))	
			dataToSend["mq135Alcohol"]=str("{:.4f}".format(percentmq135["ALCOHOL"]))
			dataToSend["mq135Co2"]=str("{:.4f}".format(percentmq135["CO2"]))
			dataToSend["mq135Nh4"]=str("{:.4f}".format(percentmq135["NH4"]))
			dataToSend["mq135Co"]=str("{:.4f}".format(percentmq135["CO"]))	

			dataToSend["mq6Raw"]=str("{:.4f}".format(percentmq6["RAW_VALUE"]))		
			dataToSend["mq6Lpg"]=str("{:.4f}".format(percentmq6["LPG"]))	
			dataToSend["mq6Ch4"]=str("{:.4f}".format(percentmq6["CH4"]))
			dataToSend["mq6H2"]=str("{:.4f}".format(percentmq6["H2"]))
			dataToSend["mq6Co"]=str("{:.4f}".format(percentmq6["CO"]))

			dataToSend["mq7Raw"]=str("{:.4f}".format(percentmq7["RAW_VALUE"]))
			dataToSend["mq7H2"]=str("{:.4f}".format(percentmq7["H2"]))
			dataToSend["mq7Co"]=str("{:.4f}".format(percentmq7["CO"]))		
			dataToSend["mq7Lpg"]=str("{:.4f}".format(percentmq7["LPG"]))
			dataToSend["mq7Ch4"]=str("{:.4f}".format(percentmq7["CH4"]))
			dataToSend["mq7Alcohol"]=str("{:.4f}".format(percentmq7["ALCOHOL"]))

			dataToSend["mq8Raw"]=str("{:.4f}".format(percentmq8["RAW_VALUE"]))
			dataToSend["mq8H2"]=str("{:.4f}".format(percentmq8["H2"]))
			dataToSend["mq8Alcohol"]=str("{:.4f}".format(percentmq8["ALCOHOL"]))
			dataToSend["mq8Lpg"]=str("{:.4f}".format(percentmq8["LPG"]))
			dataToSend["mq8Ch4"]=str("{:.4f}".format(percentmq8["CH4"]))
			dataToSend["mq8Co"]=str("{:.4f}".format(percentmq8["CO"]))

			dataToSend["mq9Raw"]=str("{:.4f}".format(percentmq9["RAW_VALUE"]))
			dataToSend["mq9Co"]=str("{:.4f}".format(percentmq9["CO"]))
			dataToSend["mq9Lpg"]=str("{:.4f}".format(percentmq9["LPG"]))
			dataToSend["mq9Ch4"]=str("{:.4f}".format(percentmq9["CH4"]))

			if 	humidityValue != "" and tempValue != "":
				dataToSend["humidity"]=humidityValue
				dataToSend["temperature"]=tempValue
				dataToSend["moduleId"]=moduleId
				#elküldendő adatok kiíratása a terminal-ban.
				print(dataToSend)
				#fejléchez csatolandó kulcs formázása.
				headersAuth = { xxxxx }
				#adatok küldése a szerverhez.
				r = requests.post('xxxxx', headers=headersAuth , json=dataToSend)
				print("sent")
				print(r.content)
				#soros csatorna pufferének és az értékeket tartalmazó válzozókna az ürítése.
				ser.reset_input_buffer()
				print("input resetted")
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
				#5 perc várakozás
				print("Sleep for 300 sec..\n\n")
				time.sleep(300)
		except BaseException as e:
			print(str(e))			

	
