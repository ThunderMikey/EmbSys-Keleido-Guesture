import tkinter
from PIL import ImageTk,Image
import subprocess
import time
import paho.mqtt.subscribe as mqtt
import json

root = tkinter.Tk()
label = tkinter.Label(root)
label.pack()
img = None
tkimg = [None]  # This, or something like it, is necessary because if you do not keep a reference to PhotoImage instances, they get garbage collected.

delay = 500   # in milliseconds

def loopCapture():
    print ("capturing")
    number_of_frame = 0
    number_of_frame = choosePic()
    img = Image.open("Pic/giphy-"+str(number_of_frame)+".png")
    tkimg[0] = ImageTk.PhotoImage(img)
    label.config(image=tkimg[0])
    root.update_idletasks()
    root.after(delay, loopCapture())

def choosePic():
    accPosition = mqtt.simple("keleido/acc",qos = 2,hostname = "192.168.0.10")
    flexAngle = mqtt.simple("keleido/flex",qos = 2, hostname = "192.168.0.10")
    accJson = json.loads(str(accPosition.payload,'utf-8'))
    flexJson = json.loads(str(flexAngle.payload,'utf-8'))
    print(accJson)
    print(flexJson)
    Angle = flexJson['angle']
    z = accJson['z']
    y = accJson['y']

    if z >= 8 :
        number_of_frame = 0
    elif z <= -8 :
        number_of_frame = 2
    elif y >= 8 :
        number_of_frame = 3
    elif y <= 8 :
        number_of_frame = 1
    else:
        number_of_frame = 0
    return number_of_frame

loopCapture()

root.mainloop()
