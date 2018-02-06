import pyautogui
import paho.mqtt.client as mqtt
#pyautogui.FAILSAFE = True

#get the screen size

#pyautogui.size()
#2560,1440

width, height = pyautogui.size()

pyautogui.alert(text='would you like to connect to ESP8266?', title='connection', button='OK')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("keleido/flex")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if int(str(msg.payload)) >= 10:
        print("click")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.10", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

# pyautogui.PAUSE = 2
#
# pyautogui.click(601,527)
# #  pyautogui.typewrite('Hello world!', 0.25)
#
# for i in range (100):
#     pyautogui.press('space')

# pyautogui.keyDown('winleft')
# pyautogui.press('s')
# pyautogui.keyUp('winleft')




pyautogui.PAUSE = 1.5
#pyautogui.typewrite('Hello world!', 0.25)
#pyautogui.typewrite('Hello world!', 0.25)
