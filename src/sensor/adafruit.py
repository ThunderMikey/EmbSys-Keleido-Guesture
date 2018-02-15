from machine import Pin, I2C
from umqtt.simple import MQTTClient
#import system
import network
import ujson
import time
import webrepl
import machine
# accelerometer
from lis3dh import LIS3DH

class Keleido:
    def __init__(self, wifiName, wifiPasswd, flexTopic, accTopic, BrokerIP,
            flexSclPin=5, flexSdaPin=4,
            accSclPin=0, accSdaPin=16,
            wifiLEDPin=2):

        # constants declaration
        self.BrokerIP = BrokerIP
        self.flexTopic = flexTopic
        self.accTopic = accTopic

        # connnect Wifi
        (self.apIf, self.staIf) = self.connectToWifi(wifiName, wifiPasswd)
        
        # init flex sensor
        self.i2c_flex = self.initFlexSensor(flexSclPin, flexSdaPin)

        # init accelerometer
        self.lis3dh = LIS3DH(accSclPin,accSdaPin)

        # init WiFi LED indicator, active low
        self.wifiLED = Pin(wifiLEDPin, Pin.OUT)
        self.wifiLED.on()

        while(self.staIf.isconnected() != True):
            pass

        # turn on WiFi LED
        self.wifiLED.off()

        self.printWifiStatus()

        # mqtt client init
        self.mqttClient = MQTTClient(machine.unique_id(),self.BrokerIP)
        self.mqttClient.connect()

        self.enableWebREPL()

    def initFlexSensor(self, flexSclPin, flexSdaPin):

        i2c_flex = I2C(scl=Pin(flexSclPin), sda=Pin(flexSdaPin), freq=100000)
        i2cportNo = i2c_flex.scan()
        self.ADSAddr = i2cportNo[0]

        # write to config register 0x01
        # CONTINUOUS_READ=0000 010 0 100 0 0 0 11
        CONTINUOUS_READ=bytearray([0b01000100, 0b10000011])
        #CONTINUOUS_READ=bytearray([0b00100100, 0b10000011])
        #CONTINUOUS_READ=bytearray([0x24, 0x83])
        print(CONTINUOUS_READ)
        i2c_flex.writeto_mem(self.ADSAddr, 1, CONTINUOUS_READ)

        return i2c_flex

    def readFlexData(self):
        # read 2 bytes from conversion register
        return self.i2c_flex.readfrom_mem(self.ADSAddr, 0, 2)

    def readAccData(self):
        """ output acceleration in x y z direction """
        return self.lis3dh.acceleration()

    def convertData(self):
        """ read raw data and convert into somthing meaningful """

        data = self.readFlexData()
        intData = int.from_bytes(data, 'big')
        print(intData)

# """
#         if intData >= 26800:
#            #angleOfFlex = 200
#         elif intData > 25000:
#             #angleOfFlex = int (((intData-25000)/90)+180)
#         elif intData > 12500:
#             #angleOfFlex = int (((intData-12500)/138)+90)
#         elif intData > 8600:
#             angleOfFlex = int ((intData-8600)/43)
#             temperature has some effect??? not very much though
#         else:
#             angleOfFlex = 0
# """

# """
#         if intData >= 15500:
#             angleOfFlex = 200
#         elif intData > 14700:
#             angleOfFlex = int (((intData-14700)/40)+180)
#         elif intData > 9500:
#             angleOfFlex = int (((intData-9500)/57)+90)
#         elif intData > 7200:
#             angleOfFlex = int ((intData-7200)/25)
#         else:
#             angleOfFlex = 0
# """
        if intData >= 2330:
            angleOfFlex = 180
        elif intData > 1700:
            angleOfFlex = int ((intData-1700)/3.5)
        else:
            angleOfFlex = 0

        print(angleOfFlex)

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
        print ("WiFi connecting... ")
        return (ap_if, sta_if)

    def printWifiStatus(self):
        print ("wiFi is connected? ", self.staIf.isconnected() )
        print ("WiFi status: ", self.staIf.status(),
                "WiFi config: ", self.staIf.ifconfig())

    def enableWebREPL(self):
        webrepl.start()

    def broadcastData(self, topic, data=bytes("random data heyheyhey",'utf-8')):
        """ publish data in bytes
        """
        self.mqttClient.publish(topic, data)

    def broadcastString(self, inString="No input string\n"):
        """ publish data in string
        """
        data = bytes(inString, 'utf-8')
        self.broadcastData(data)

    def doBatchJob(self):
        # flex sensor
        flexData = {}
        flexData["angle"] = self.convertData()
        #print(flexData)
        flexDataJsonString = ujson.dumps(flexData)
        flexDataByte = bytes(flexDataJsonString, 'utf-8')
        self.broadcastData(self.flexTopic, flexDataByte)

        # accelerometer
        accData = {}
        (x,y,z) = self.readAccData()
        accData['x'] = x
        accData['y'] = y
        accData['z'] = z
        accDataByte = bytes(ujson.dumps(accData), 'utf-8')
        self.broadcastData(self.accTopic, accDataByte)
