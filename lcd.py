from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd

i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)
