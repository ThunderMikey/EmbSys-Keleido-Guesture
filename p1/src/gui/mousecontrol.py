import pyautogui
import paho.mqtt.subscribe as mqtt
import json
#pyautogui.FAILSAFE = True

#get the screen size

#pyautogui.size()
#2560,1440


width, height = pyautogui.size()

pyautogui.alert(text='would you like to connect to ESP8266?', title='connection', button='OK')

data = mqtt.simple("keleido/acc",hostname = "192.168.0.10")
print(str(data.payload,'utf-8'))
# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))
#
#     # Subscribing in on_connect() means that if we lose the connection and
#     # reconnect then subscriptions will be renewed.
#     client.subscribe("keleido/acc")
#
# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     #print(msg.topic+" "+ str(msg.payload,'utf-8'))
#     data = json.loads(str(msg.payload,'utf-8'))
#     # print(data['angle'])
#     # if data['angle'] <= 60:
#     #     pyautogui.keyDown('space')
#     # else :
#     #     pyautogui.keyUp('space')
#     return msg
#     # elif down == True:
#     #     down = False
#     #     pyautogui.typewrite('H')
#     #     pyautogui.PAUSE = 1
#
#
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
#
# client.connect("192.168.0.10", 1883, 60)
#
# # client.loop_forever()
#
# run = True
# while run:
#     client.loop()
#     print(client.msg())
# pyautogui.PAUSE = 2
#
# pyautogui.click(601,527)
# pyautogui.typewrite('Hello world!', 0.25)
#
# for i in range (10):
#     pyautogui.press('space')
#     pyautogui.PAUSE = 1.0
# pyautogui.keyDown('winleft')
# pyautogui.press('s')
# pyautogui.keyUp('winleft')



#pyautogui.typewrite('Hello world!', 0.25)
#pyautogui.typewrite('Hello world!', 0.25)
