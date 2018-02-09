from adafruit import Keleido

magic = Keleido(wifiName="EEERover", wifiPasswd="exhibition", topic="keleido/flex", BrokerIP = "192.168.0.10", servoPin=14, LEDPin=4)

while 1 :
    magic.receiveData()
