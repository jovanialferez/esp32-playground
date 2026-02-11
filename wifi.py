import network
import utime
import ntptime
import machine
from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd

SSID = "free-wifi"
PASSWORD = "123456qwerty"
UTC_OFFSET = 8 * 3600 

# Keep the global objects so other files can use them
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, i2c.scan()[0], 2, 16)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    lcd.clear()
    lcd.putstr("WiFi: Connecting")
    
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        for _ in range(10):
            if wlan.isconnected(): break
            utime.sleep(1)

    if wlan.isconnected():
        try:
            ntptime.settime()
            rtc = machine.RTC()
            tm = utime.localtime(utime.time() + UTC_OFFSET)
            # Sets the hardware clock
            rtc.datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
            return wlan.ifconfig()[0]
        except:
            return wlan.ifconfig()[0]
    return "No Connection"
