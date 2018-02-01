from machine import Pin, I2C
from umqtt.simple import MQTTClient
import system
import network

class Keleido:
    def __init__(self):
        self.meaningfulData = 0
        self.connectToWifi()

    def packIntoJSON(self):


    def convertData(self):
        """ read raw data and convert into somthing meaningful """


    def connectToWifi(self):
