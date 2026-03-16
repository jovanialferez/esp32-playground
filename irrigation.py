from machine import ADC, Pin
import utime

# How dry the soil needs to be before we water it.
# ADC reads 0 (wet) to 4095 (dry). Higher number = drier soil.
DRY_THRESHOLD = 2200

# Max seconds a pump can run in one go — prevents flooding if a sensor breaks.
MAX_SAFETY_TIME = 10

def run():
    # Set up 4 soil moisture sensors on pins 32, 33, 34, 35.
    # ADC (Analog-to-Digital Converter) reads voltage as a number 0–4095.
    sensors = [ADC(Pin(p)) for p in [32, 33, 34, 35]]
    for s in sensors:
        # ATTN_11DB allows reading the full 0–3.3V range from the sensor.
        s.atten(ADC.ATTN_11DB)

    # Set up 4 water pumps on pins 26, 27, 14, 12.
    # value=1 means OFF at start — these pumps are "Active Low" (0 = ON, 1 = OFF).
    pumps = [Pin(p, Pin.OUT, value=1) for p in [26, 27, 14, 12]]

    print("System Online: Continuous Feedback Mode")

    try:
        while True:
            # Check each plant one by one (i = 0, 1, 2, 3)
            for i in range(4):
                moisture = sensors[i].read()  # Read soil moisture (0–4095)

                if moisture > DRY_THRESHOLD:  # Soil is too dry — needs water
                    print("Plant {} is DRY ({}). Watering...".format(i + 1, moisture))
                    start_time = utime.time()  # Record when we started pumping

                    # Keep watering until soil is moist enough OR time limit is hit
                    while sensors[i].read() > DRY_THRESHOLD:
                        pumps[i].value(0)   # Turn pump ON (Active Low)
                        utime.sleep(0.1)    # Wait 0.1s then re-check the sensor

                        # Safety check: stop pump if it's been running too long
                        if (utime.time() - start_time) > MAX_SAFETY_TIME:
                            print("!! SAFETY TIMEOUT on Plant {} !!".format(i + 1))
                            break

                    pumps[i].value(1)  # Turn pump OFF
                    print("Plant {} reached threshold. Pump stopped.".format(i + 1))

                else:
                    # Soil moisture is fine, no action needed
                    print("Plant {}: OK ({})".format(i + 1, moisture))

            print("--- All plants checked. Waiting 5s ---")
            utime.sleep(5)  # Wait 5 seconds before checking all plants again

    except KeyboardInterrupt:
        # If the user presses Ctrl+C, make sure all pumps are turned OFF safely
        for p in pumps:
            p.value(1)
        print("Emergency Stop.")
