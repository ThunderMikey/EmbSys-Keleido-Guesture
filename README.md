# 3nd Year Embedded Systems IOT Coursework

## Group Name: Keleido

## Product: Guesture Reconstruction with its Applications Using Flex and Other Sensor
The product takes input from a single flex sensor with an additional accelerometer and transmit the information via MQTT and the data format is JSON, the information is then subscribed by multiply devices to further process the information. In this repository there are a few demo in the folder src/gui, but the application is unlimited and here is just a glance of what the technology can be applied to.   
### Team Members: 
Mike Chen (yc12015): https://github.com/ThunderMikey/

Zeqian Cao (zc3515): https://github.com/kuzhankuixiong

Zihan Liu (zl6114): https://github.com/zl6114

### Product Website
https://zc3515.wixsite.com/kaleido

### Sensor Used
FS7548 flex sensor with ADS1115 ADC  

LIS3DH accelerometer 

Adafruit Feather HUZZAH ESP8266

# Directory structure

```
|
src
   \
   gui:    mouse control on PC side
   	     MQTT receive side
   |
   sensor: flex sensor and accelerometer, ESP board
   		MQTT send side
   |
   motor: servo receiving flex angle, ESP board
   		MQTT receive side
|
doc: lab instructions
|
README.md: this file
|
demo.md: demo script
```
# Connection details

### Get WebREPL
`git clone https://github.com/micropython/webrepl.git`

### Open WebREPL in browser
passwrd: `Keleido`

# Docs
[first lab](./docs/lab-instructions-i2c.pdf)

[MicroPython official support webapge](http://docs.micropython.org/en/v1.8.2/esp8266/esp8266/tutorial/index.html)

[ampy official doc](https://cdn-learn.adafruit.com/downloads/pdf/micropython-basics-load-files-and-run-code.pdf)

[ADS1115 data sheet](http://www.ti.com/lit/ds/symlink/ads1115.pdf)

[FS7548 data sheet](https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/FLEXSENSORREVA1.pdf)

[Adafruit Feather HUZZAH ESP8266](https://cdn-learn.adafruit.com/assets/assets/000/046/211/original/Huzzah_ESP8266_Pinout_v1.2.pdf)


### Run python script
`ampy -p $AMPY_PORT run`

### Copy script to the MSP
`ampy -p $AMPY_PORT put`

### List files in the MSP
`ampy -p $AMPY_PORT ls`

# Coursewok1 info

## Deliverables
* Demo showing sensing, processing and upload of data
* Code submission via GitHub
* Website marketing concept for product

## Timescale
* This week: lab on sensor communication
* Next week: lab on MQTT
* Week after that: lab time on project
* Week after that: demo, code and website submission

# Adafruit Feather HUZZAH ESP8266
![adafruit front](https://cdn-learn.adafruit.com/assets/assets/000/028/699/original/adafruit_products_2821_top_01_ORIG.jpg)

![adafruit back](https://cdn-learn.adafruit.com/assets/assets/000/028/700/original/adafruit_products_2821_back_ORIG.jpg)










