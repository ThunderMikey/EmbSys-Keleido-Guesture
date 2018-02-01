from machine import Pin, I2C
from umqtt.simple import MQTTClient
import system
import network
import ujson
import time 

class Keleido:
    def __init__(self):
        self.meaningfulData = 0
        self.connectToWifi()

    def packIntoJSON(self):
	data = {}
	data["DataType"] = "Unknown"
	data["value"] = self.meaningfulData
	encoded = ujson.dumps(data)
	print(encoded)


    def convertData(self):
        """ read raw data and convert into somthing meaningful """


    def connectToWifi(self):
