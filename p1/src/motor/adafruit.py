from machine import Pin, I2C, PWM
from umqtt.simple import MQTTClient
#import system
import network
import ujson
import time
import webrepl
import machine

class Servo:
    def __init__(self, servoPin):
        self.servo = PWM(Pin(servoPin), freq=50, duty=77)
        self.medianFilterSize = 7
        self.FIFO = [77]*self.medianFilterSize

    def turnServo(self, in_dutyCycle):
        """ The center is at around 78, and the exact range varies with the servo model,
            but should be somewhere between 25 and 125, which corresponds to about 180° of movement.
        """
        medianIdx = int(len(self.FIFO)/2)
        self.FIFO.pop(0)
        self.FIFO.append(in_dutyCycle)
        # copy the FIFO
        medianFilterList = list(self.FIFO)
        # sort list
        medianFilterList.sort()
        # choose median value
        dutyCycle = medianFilterList[medianIdx]
        if dutyCycle >= 25 and dutyCycle <= 125 :
            self.servo.duty(dutyCycle)
        else:
            print("{0} is too big, range (25, 125)".format(dutyCycle))


class Keleido:
    def __init__(self, wifiName, wifiPasswd, topic_flex, topic_acc, BrokerIP, flexServoPin=14, LEDPin=4, accxServoPin=0, accyServoPin=16):
        self.BrokerIP = BrokerIP
        self.topic_flex = topic_flex
        self.topic_acc = topic_acc
        self.flexServoPin = flexServoPin
        self.LEDPin = LEDPin

        self.medianFilterSize = 7
        self.flexAngleFIFO = [180]*self.medianFilterSize

        # WiFi interface
        (self.apIf, self.staIf) = self.connectToWifi(wifiName, wifiPasswd)

        # servo interface
        self.flexServo = PWM(Pin(self.flexServoPin), freq=50, duty=77)
        self.accxServo = PWM(Pin(self.accxServoPin), freq=50, duty=77)
        self.accyServo = PWM(Pin(self.accyServoPin), freq=50, duty=77)

        # LED WiFi status indicator, LED is active low
        self.LED_WifiConnected = Pin(self.LEDPin, Pin.OUT)
        self.LED_WifiConnected.on()

        # ensure WiFi is connected
        while(self.staIf.isconnected() != True):
            pass
        # print WiFi info
        self.getWifiStatus()

        # WiFi connected, turn LED on, active low
        self.LED_WifiConnected.off()

        # MQTT interface
        self.mqttClient = MQTTClient(machine.unique_id(),self.BrokerIP)
        self.mqttClient.connect()
        self.mqttClient.set_callback(self.setMotorAngle)
        self.mqttClient.subscribe(self.topic_flex)

        # enable WebREPL
        self.enableWebREPL()


    def connectToWifi(self, wifiName, password):
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(wifiName, password)

        # print wifi info
        print ("WiFi connecting...")
        return (ap_if, sta_if)

    def getWifiStatus(self):
        print ("wiFi is connected? ", self.staIf.isconnected() )
        print ("WiFi status: ", self.staIf.status(),
                "WiFi config: ", self.staIf.ifconfig())

    def enableWebREPL(self):
        print( webrepl.start() )

    def receiveData(self):
        self.mqttClient.check_msg()
        #self.mqttClient.wait_msg()

    def setMotorAngle(self, rawTopic, rawData):
        """ decode received msg and turn motor """
        topic = bytes.decode(rawTopic, 'utf-8')
        msg = bytes.decode(rawData, 'utf-8')
        print("msg received ", topic, msg)

        msgJson = ujson.loads(msg)
        multFactor = 100/180
        # flexAngle should between (0, 180)
        flexAngle = msgJson['angle']
        # median filter to remove jitter
        medianIdx = int(len(self.flexAngleFIFO)/2)
        self.flexAngleFIFO.pop(0)
        self.flexAngleFIFO.append(flexAngle)
        # copy the FIFO
        flexAngleMF = list(self.flexAngleFIFO)
        # sort list
        flexAngleMF.sort()
        # choose median value
        flexAngle = flexAngleMF[medianIdx]
        # debug output
        #print(self.flexAngleFIFO)

        if flexAngle <= 180 and flexAngle >= 0:
            servoAngle = int(25 + flexAngle*multFactor)
            self.turnServo(servoAngle)
        else:
            print("flex angle should be (0, 180), but it is: {0}".format(flexAngle))

    def broadcastString(self, inString="No input string\n"):
        data = bytes(inString, 'utf-8')
        self.broadcastData(data)

    def turnServo(self, angle):
        """ The center is at around 78, and the exact range varies with the servo model,
            but should be somewhere between 25 and 125, which corresponds to about 180° of movement.
        """
        if angle >= 25 and angle <= 125 :
            self.flexServo.duty(angle)
        else:
            print("{0} is too big, range (25, 125)".format(angle))

