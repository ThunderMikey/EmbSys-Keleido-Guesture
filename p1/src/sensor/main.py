from adafruit import Keleido
import time

magic = Keleido(wifiName="EEERover", wifiPasswd="exhibition", topic="keleido/flex", BrokerIP = "192.168.0.10")

while 1 :
    """ send flex angle with freq of 20Hz
    """
    rawData = magic.prepareData()
    magic.broadcastData(data=rawData)
    time.sleep(0.05)


