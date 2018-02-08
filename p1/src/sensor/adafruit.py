from machine import Pin, I2C
from umqtt.simple import MQTTClient
#import system
import network
import ujson
import time 
import webrepl
import machine

class Keleido:
    def __init__(self, wifiName, wifiPasswd, topic, BrokerIP):
        self.meaningfulData = 0
        self.BrokerIP = BrokerIP
        self.topic = topic
        (self.apIf, self.staIf) = self.connectToWifi(wifiName, wifiPasswd)
        while(self.staIf.isconnected() != True):
            pass
        self.enableWebREPL()

    def packIntoJSON(self):
	data = {}
	data["DataType"] = "AngleOfFlex(0-22)"
	data["value"] = self.convertData()
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
        if intData > 7200:
            angleOfFlex = 180
        elif intData > 3000 :
            angleOfFlex = int ((intData-2000)/28) #7200
        else:
            angleOfFlex = int (intData/22)

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
        sta_if.connect(wifiName, password)
 
        # print wifi info
        print ("WiFi status: ", sta_if.status(), 
                "WiFi config: ", sta_if.ifconfig())
        return (ap_if, sta_if)

    def getWifiStatus(self):
        print ("wiFi is connected? ", self.staIf.isconnected() )
        print ("WiFi status: ", self.staIf.status(), 
                "WiFi config: ", self.staIf.ifconfig())

    def enableWebREPL(self):
        print( webrepl.start() )

    def broadcastData(self, data=bytes("random data heyheyhey",'utf-8')):
        client = MQTTClient(machine.unique_id(),self.BrokerIP)
        client.connect()
        client.publish(self.topic, data)

    def broadcastString(self, inString="No input string\n"):
        data = bytes(inString, 'utf-8')
        self.broadcastData(data)
