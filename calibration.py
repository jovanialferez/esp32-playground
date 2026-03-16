from machine import ADC, Pin
import utime
import lcd as _lcd

def run():
    sensor = ADC(Pin(32))
    sensor.atten(ADC.ATTN_11DB)

    while True:
        moisture = sensor.read()
        print("Probe 1: {}".format(moisture))

        _lcd.lcd.move_to(0, 0)
        _lcd.lcd.putstr("{:<16}".format("Probe 1 Cal."))
        _lcd.lcd.move_to(0, 1)
        _lcd.lcd.putstr("{:<16}".format("Val: {}".format(moisture)))

        utime.sleep(1)
