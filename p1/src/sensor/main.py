from adafruit import Keleido
import time

magic = Keleido(wifiName="EEERover", wifiPasswd="exhibition", BrokerIP = "192.168.0.10",
                flexTopic="keleido/flex", accTopic="keleido/acc",
                flexSclPin=5, flexSdaPin=4,
                accSclPin=0, accSdaPin=16)

while 1 :
    """ send flex angle and accelerometer at freq of 20Hz
    """
    magic.doBatchJob()
    time.sleep(0.05)


