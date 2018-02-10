from adafruit import Keleido
import time


""" pin 1 will cause system to be not respond to REPL
"""
magic = Keleido(wifiName="EEERover", wifiPasswd="exhibition", topic="keleido/flex", BrokerIP = "192.168.0.10", servoPin=14, LEDPin=4)

while 1 :
    """ on receiving data, call_back setMotorAngle()
        update at 20Hz frequency
    """
    magic.receiveData()
    time.sleep(0.05)

