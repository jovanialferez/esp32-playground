import utime
import wifi


def run():
    ip_address = wifi.connect_wifi()

    while True:
        t = utime.localtime()
        date_str = "{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(t[1], t[2], t[3], t[4], t[5])

        wifi.lcd.clear()
        wifi.lcd.move_to(0, 0)
        wifi.lcd.putstr(ip_address)
        wifi.lcd.move_to(0, 1)
        wifi.lcd.putstr(date_str)

        utime.sleep(1)
