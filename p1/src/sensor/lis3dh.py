from machine import Pin, I2C
from umqtt.simple import MQTTClient
#import system
import network
import ujson
import time
import webrepl
import machine
import ustruct

# Register value constants:
# refrenece to
RANGE_16_G               = const(0b11)    # +/- 16g
RANGE_8_G                = const(0b10)    # +/- 8g
RANGE_4_G                = const(0b01)    # +/- 4g
RANGE_2_G                = const(0b00)    # +/- 2g (default value)
DATARATE_1344_HZ         = const(0b1001)  # 1.344 KHz
DATARATE_400_HZ          = const(0b0111)  # 400Hz
DATARATE_200_HZ          = const(0b0110)  # 200Hz
DATARATE_100_HZ          = const(0b0101)  # 100Hz
DATARATE_50_HZ           = const(0b0100)  # 50Hz
DATARATE_25_HZ           = const(0b0011)  # 25Hz
DATARATE_10_HZ           = const(0b0010)  # 10 Hz
DATARATE_1_HZ            = const(0b0001)  # 1 Hz
DATARATE_POWERDOWN       = const(0)
DATARATE_LOWPOWER_1K6HZ  = const(0b1000)
DATARATE_LOWPOWER_5KHZ   = const(0b1001)

REG_OUTADC1_L   = const(0x08)
REG_WHOAMI      = const(0x0F)
REG_TEMPCFG     = const(0x1F)
REG_CTRL1       = const(0x20)
REG_CTRL3       = const(0x22)
REG_CTRL4       = const(0x23)
REG_CTRL5       = const(0x24)
REG_OUT_X_H     = const(0x29)
REG_OUT_X_L     = const(0x28)
FIFO_CTRL_REG   = const(0x2E)
INT1_CFG        = const(0x30)
REG_INT1SRC     = const(0x31)
REG_CLICKCFG    = const(0x38)
REG_CLICKSRC    = const(0x39)
REG_CLICKTHS    = const(0x3A)
REG_TIMELIMIT   = const(0x3B)
REG_TIMELATENCY = const(0x3C)
REG_TIMEWINDOW  = const(0x3D)

# Other constants
STANDARD_GRAVITY = 9.806

class LIS3DH:
    #Driver for LIS3DH accelerometer.
    def __init__(self,int1 = None,int2 = None):
        self.int1 = int1
        self.int2 = int2
        #set up I2C
        self.i2c_lis3dh = I2C(scl=Pin(int1), sda=Pin(int2), freq=100000)
        #scan for i2cportNo
        i2cportNo = self.i2c_lis3dh.scan()
        AccAddr = i2cportNo[0]
        # Enable all axes, normal mode, REG_CTRL1
        self.i2c_lis3dh.writeto_mem(AccAddr,REG_CTRL1,bytearray([0x97]))
        # High res & BDU enabled. REG_CTRL4
        # RANGE_2_G
        self.i2c_lis3dh.writeto_mem(ADSAddr,REG_CTRL4,bytearray([0x88]))

    def acceleration(self):
        i2cportNo = self.i2c_lis3dh.scan()
        AccAddr = i2cportNo[0]
        divider = 16380
        x = self.i2c_lis3dh.readfrom_mem(AccAddr, REG_OUT_X_L  | 0x80, 2)
        # convert from Gs to m / s ^ 2 and adjust for the range
        x = int.from_bytes(x, 'big')
        x = (x / divider) * STANDARD_GRAVITY
        # y = (y / divider) * STANDARD_GRAVITY
        # z = (z / divider) * STANDARD_GRAVITY
        return x

        # Enable all axes, normal mode, REG_CTRL1
        # self.i2c_lis3dh.writeto_mem(AccAddr,REG_CTRL1,bytearray(0x97))
        # self.i2c_lis3dh.writeto_mem(AccAddr,REG_CTRL4,bytearray(0x08))
        # # High res & BDU enabled. REG_CTRL4
        # # RANGE_2_G
        # self.i2c_lis3dh.writeto_mem(ADSAddr,REG_CTRL4,bytearray(0x88))
        # self.i2c_lis3dh.writeto_mem(ADSAddr,REG_CTRL3,bytearray(0x10))
        # # Enable ADCs.REG_TEMPCFG
        # self.i2c_lis3dh.writeto_mem(ADSAddr,REG_TEMPCFG,bytearray(0x80))
        # # Latch interrupt for INT1
        # self.i2c_lis3dh.writeto_mem(ADSAddr,REG_CTRL5,bytearray(0x00))
        # # Set interrupt
        # self.i2c_lis3dh.writeto_mem(ADSAddr,FIFO_CTRL_REG,bytearray(0x40))
