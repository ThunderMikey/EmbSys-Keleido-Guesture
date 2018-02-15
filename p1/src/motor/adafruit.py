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
    def __init__(self, wifiName, wifiPasswd, topic_flex, topic_acc, BrokerIP, flexServoPin=14, LEDPin=4, accxServoPin=0, accyServoPin=15):
        self.BrokerIP = BrokerIP
        self.topic_flex = topic_flex
        self.topic_acc = topic_acc
        self.LEDPin = LEDPin

        # WiFi interface
        (self.apIf, self.staIf) = self.connectToWifi(wifiName, wifiPasswd)

        # servo interface
        self.flexServo = Servo(flexServoPin)
        self.acczServo = Servo(accxServoPin)
        self.accyServo = Servo(accyServoPin)

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

        # MQTT flex
        self.mqttClient_flex = MQTTClient(machine.unique_id(),self.BrokerIP)
        self.mqttClient_flex.connect()
        self.mqttClient_flex.set_callback(self.flexCallback)
        #self.mqttClient_flex.subscribe(self.topic_flex)
        self.mqttClient_flex.subscribe(['keleido/flex', 'keleido/acc'])

        # MQTT accelerometer
        #self.mqttClient_acc = MQTTClient(machine.unique_id(),self.BrokerIP)
        #self.mqttClient_acc.connect()
        #self.mqttClient_acc.set_callback(self.accCallback)
        #self.mqttClient_acc.subscribe(self.topic_acc)

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
        """" unblocking checkout msg call """
        self.mqttClient_flex.check_msg()
        #self.mqttClient_acc.check_msg()
        #self.mqttClient.wait_msg()

    def flexCallback(self, rawTopic, rawData):
        """ decode received msg and turn servo """
        topic = bytes.decode(rawTopic, 'utf-8')
        msg = bytes.decode(rawData, 'utf-8')
        print("msg received ", topic, msg)

        #msgs = msg.splitlines()
        #print(msgs)
        msgJson = ujson.loads(msgs)
        multFactor = 100/180
        # flexAngle should between (0, 180)
        flexAngle = msgJson['angle']

        if flexAngle <= 180 and flexAngle >= 0:
            servoAngle = int(25 + flexAngle*multFactor)
            self.flexServo.turnServo(servoAngle)
        else:
            print("flex angle should be (0, 180), but it is: {0}".format(flexAngle))

    def accCallback(self, rawTopic, rawData):
        """ decode accelerometer msg and turn servo """
        msg = bytes.decode(rawData, 'uft-8')

        msgJson = ujson.loads(msg)
        acc_z = msgJson['z']
        acc_y = msgJson['y']

        # support acc range (-20, 20)
        multFactor = 100/40
        acczDuty = int(77 + acc_z*multFactor)
        accyDuty = int(77 + acc_y*multFactor)
        self.acczServo.turnServo(acczDuty)
        self.accyServo.turnServo(accyDuty)

