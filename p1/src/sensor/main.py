from adafruit import Keleido
from lis3dh import LIS3DH

magic = Keleido(wifiName="EEERover", wifiPasswd="exhibition", topic="keleido/flex", BrokerIP = "192.168.0.10")
magic.broadcastString("this is a message")

Lis3dh = LIS3DH()
print(Lis3dh.acceleration())
