from machine import Pin, I2C
from umqtt.simple import MQTTClient
#import system
import network
import ujson
import time
import webrepl
import machine
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

class LIS3DH:
    #Driver for LIS3DH accelerometer.
    def __init__(self, int1=None, int2=None):
        # Check device ID. 0x0F is the Who I Am register
        device_id = self._read_register_byte(0x0F)
        if device_id != 0x33:
            raise RuntimeError('Failed to find LIS3DH!')
        # Set Reboot flag of Control 5 Register (0x24) high
        self._write_register_byte(0x24, 0x80)
        time.sleep(0.01)  # takes 5ms
        # Enable all axes, normal mode, REG_CTRL1
        self._write_register_byte(0x20, 0x07)
        # Set 400Hz data rate.
        self.data_rate = DATARATE_400_HZ
        # High res & BDU enabled. REG_CTRL4
        self._write_register_byte(0x23, 0x88)
        # Enable ADCs.REG_TEMPCFG
        self._write_register_byte(0x1F, 0x80)
        # Latch interrupt for INT1, reg crontol 5
        self._write_register_byte(0x24, 0x08)
    def acceleration(self):
        """The x, y, z acceleration values returned in a 3-tuple and are in m / s ^ 2."""
        divider = 1
        accel_range = self.range
        if accel_range == RANGE_16_G:
            divider = 1365
        elif accel_range == RANGE_8_G:
            divider = 4096
        elif accel_range == RANGE_4_G:
            divider = 8190
        elif accel_range == RANGE_2_G:
            divider = 16380

        x, y, z = struct.unpack('<hhh', self._read_register(REG_OUT_X_L | 0x80, 6))

        # convert from Gs to m / s ^ 2 and adjust for the range
        x = (x / divider) * STANDARD_GRAVITY
        y = (y / divider) * STANDARD_GRAVITY
        z = (z / divider) * STANDARD_GRAVITY

        return x, y, z
