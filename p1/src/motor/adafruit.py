from machine import Pin, I2C, PWM
from umqtt.simple import MQTTClient
#import system
import network
import ujson
import time 
import webrepl
import machine

class Keleido:
    def __init__(self, wifiName, wifiPasswd, topic, BrokerIP, servoPin=14):
        self.meaningfulData = 0
        self.BrokerIP = BrokerIP
        self.topic = topic
        self.servoPin = servoPin

        (self.apIf, self.staIf) = self.connectToWifi(wifiName, wifiPasswd)
        
        self.servo = PWM(Pin(servoPin), freq=50, duty=77)

        while(self.staIf.isconnected() != True):
            pass
        self.enableWebREPL()

    def packIntoJSON(self):
	data = {}
	data["DataType"] = "AngleOfFlex(0-22)"
	data["value"] = self.convertData()
	encoded = ujson.dumps(data)
	return encoded

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

    def receiveData(self):
        client = MQTTClient(machine.unique_id(),self.BrokerIP)
        client.connect()
        client.set_callback(self.setMotorAngle)
        client.subscribe(self.topic)
        #msg = client.check_msg()
        msg = client.wait_msg()
        print(msg)
        return msg

    def setMotorAngle(self, rawTopic, rawData):
        topic = bytes.decode(rawTopic, 'utf-8')
        msg = bytes.decode(rawData, 'utf-8')
        print("msg received ", topic, msg)
        

    def broadcastString(self, inString="No input string\n"):
        data = bytes(inString, 'utf-8')
        self.broadcastData(data)

    def turnServo(self, angle):
        """ The center is at around 78, and the exact range varies with the servo model, 
            but should be somewhere between 25 and 125, which corresponds to about 180° of movement.
        """
        if angle >= 25 and angle <= 125 :
            self.servo.duty(angle)
        else:
            print("{0} is too big, range (25, 125)".format(angle))

