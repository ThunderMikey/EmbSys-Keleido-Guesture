from adafruit import Keleido

magic = Keleido(wifiName="EEERover", wifiPasswd="exhibition")
print ("JSON payload is: ", magic.packIntoJSON())
print ("angleOfFlex: ", magic.convertData())
magic.enableWebREPL()
