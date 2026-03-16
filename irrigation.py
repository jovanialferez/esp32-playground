from machine import ADC, Pin
import utime

DRY_THRESHOLD = 2200
MAX_SAFETY_TIME = 10

def run():
    sensors = [ADC(Pin(p)) for p in [32, 33, 34, 35]]
    for s in sensors:
        s.atten(ADC.ATTN_11DB)

    pumps = [Pin(p, Pin.OUT, value=1) for p in [26, 27, 14, 12]]

    print("System Online: Continuous Feedback Mode")

    try:
        while True:
            for i in range(4):
                moisture = sensors[i].read()

                if moisture > DRY_THRESHOLD:
                    print("Plant {} is DRY ({}). Watering...".format(i + 1, moisture))
                    start_time = utime.time()

                    while sensors[i].read() > DRY_THRESHOLD:
                        pumps[i].value(0)
                        utime.sleep(0.1)

                        if (utime.time() - start_time) > MAX_SAFETY_TIME:
                            print("!! SAFETY TIMEOUT on Plant {} !!".format(i + 1))
                            break

                    pumps[i].value(1)
                    print("Plant {} reached threshold. Pump stopped.".format(i + 1))

                else:
                    print("Plant {}: OK ({})".format(i + 1, moisture))

            print("--- All plants checked. Waiting 5s ---")
            utime.sleep(5)

    except KeyboardInterrupt:
        for p in pumps:
            p.value(1)
        print("Emergency Stop.")
