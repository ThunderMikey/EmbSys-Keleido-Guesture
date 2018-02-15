import pyautogui
import paho.mqtt.client as mqtt
import json

width, height = pyautogui.size()

#manually set up the enviorment, then after set up, press ok
pyautogui.alert(text='would you like to connect to ESP8266?', title='connection', button='OK')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("keleido/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    Data = json.loads(str(msg.payload,'utf-8'))
    # print(flexJson)
    print(Data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.10", 1883, 60)

client.loop_forever()
