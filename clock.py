import utime
import wifi
import lcd as _lcd


def run():
    ip_address = wifi.connect_wifi()

    while True:
        t = utime.localtime()
        date_str = "{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(t[1], t[2], t[3], t[4], t[5])

        _lcd.lcd.clear()
        _lcd.lcd.move_to(0, 0)
        _lcd.lcd.putstr(ip_address)
        _lcd.lcd.move_to(0, 1)
        _lcd.lcd.putstr(date_str)

        utime.sleep(1)
