import pyautogui
import paho.mqtt.subscribe as mqtt
import time
import json

pyautogui.FAILSAFE = True

#get the screen size

#pyautogui.size()
#2560,1440

down = False
global xref, yref, zref
xref, yref, zref = 0, 0, 0


width, height = pyautogui.size()

pyautogui.alert(text='would you like to connect to ESP8266?', title='connection', button='OK')
pyautogui.moveTo(width/2, height/2, duration=0.2)

def UpAndDown(position,Value):

    if abs(position) <= 9:
        return 0

    Value = abs(position) - 9

    if position > 0:
        Value = 0 - Value

    return Value*10

while 1:
    # simple MQTT receive to enable in file data process
    flexAngle = mqtt.simple("keleido/flex",qos = 2, hostname = "192.168.0.10")
    accPosition = mqtt.simple("keleido/acc",qos = 2,hostname = "192.168.0.10")

    flexJson = json.loads(str(flexAngle.payload,'utf-8'))
    accJson = json.loads(str(accPosition.payload,'utf-8'))
    # print(flexJson)
    # print(accJson)

    Angle = flexJson['angle']
    x = accJson['x']
    y = accJson['y']
    z = accJson['z']

    # print(z)

    z_movement = UpAndDown(z,0)
    y_movement = UpAndDown(y,0)

    if Angle <= 30:
        pyautogui.click()

    pyautogui.moveRel(-y*15, x*15, duration=0.2)

    if z <= -9:
        pyautogui.moveTo(width/2, height/2, duration=0.2)
