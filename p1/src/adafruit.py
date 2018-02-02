from machine import Pin, I2C
from umqtt.simple import MQTTClient
#import system
import network
import ujson
import time 

class Keleido:
    def __init__(self, wifiName, wifiPasswd):
        self.meaningfulData = 0
        (self.apIf, self.staIf) = self.connectToWifi(wifiName, wifiPasswd)

    def packIntoJSON(self):
	data = {}
	data["DataType"] = "Unknown"
	data["value"] = self.meaningfulData
	encoded = ujson.dumps(data)
	return encoded


    def convertData(self):
        """ read raw data and convert into somthing meaningful """

        i2c = I2C(scl=Pin(4), sda=Pin(5), freq=100000)
        i2cportNo = i2c.scan()
        ADSAddr = i2cportNo[0]

        # write to config register 0x01
        # CONTINUOUS_READ=0000 010 0 100 0 0 0 11
        CONTINUOUS_READ=bytearray(0b0010010010000011)

        i2c.writeto_mem(ADSAddr, 1, CONTINUOUS_READ)
        data = i2c.readfrom_mem(ADSAddr, 0, 2)
        intData = int.from_bytes(data, 'big')
        if intData > 3000 :
            angleOfFlex = int ((intData-2000)/28) #7200
        else:
            angleOfFlex = intData/22

        #print(i2cportNo)
        #print(data)
        #print(intData)
        #print(angleOfFlex)

        return angleOfFlex

    def connectToWifi(self, wifiName, password):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect('EEERover', 'exhibition')

        return (ap_if, sta_if)


