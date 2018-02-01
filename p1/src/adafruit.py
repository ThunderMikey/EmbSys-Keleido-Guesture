from machine import Pin, I2C
from umqtt.simple import MQTTClient
import system
import network

class Keleido:
    def __init__(self, wifiName, wifiPasswd):
        self.meaningfulData = 0
        (self.apIf, self.staIf) = self.connectToWifi(wifiName, wifiPasswd)

    def packIntoJSON(self):


    def convertData(self):
        """ read raw data and convert into somthing meaningful """


    def connectToWifi(self, wifiName, password):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        sta_if = network.WLAN(network.AP_IF)
        sta_if.active(True)
        sta_if.connect(wifiName, password)

        return (ap_if, sta_if)


