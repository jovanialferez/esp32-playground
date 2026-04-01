from machine import ADC, Pin
import utime
import lcd as _lcd

# --- Calibration Constants ---
# Pumping STARTS when reading is >= START_WATERING (Dry)
START_WATERING = 3134 
# Pumping STOPS when reading is <= STOP_WATERING (Wet)
STOP_WATERING = 2946  

# --- Tuning Constants for Pulse Watering ---
PULSE_ON = 1.5   # Seconds to pump
SOAK_TIME = 2.0  # Seconds to wait for water to reach sensor

# Max seconds a pump can run — crucial for capstone safety!
MAX_SAFETY_TIME = 8 

def lcd_show(row0, row1):
    _lcd.lcd.move_to(0, 0)
    _lcd.lcd.putstr("{:<16}".format(row0))
    _lcd.lcd.move_to(0, 1)
    _lcd.lcd.putstr("{:<16}".format(row1))

def run():
    # Setup Sensors (32, 33, 34, 35)
    sensors = [ADC(Pin(p)) for p in [32, 33, 34, 35]]
    for s in sensors:
        s.atten(ADC.ATTN_11DB)

    # Setup Pumps (26, 27, 14, 12) - Active Low (1=OFF, 0=ON)
    pumps = [Pin(p, Pin.OUT, value=1) for p in [26, 27, 14, 12]]

    print("System Online: Hysteresis Mode ({}-{})".format(STOP_WATERING, START_WATERING))
    lcd_show("Irrigation", "System Online")
    utime.sleep(2)

    try:
        while True:
            for i in range(4):
                current_moisture = sensors[i].read()
                
                # Check if the plant has crossed the 'DRY' trigger point
                if current_moisture >= START_WATERING:
                    print("Plant {} is DRY ({}). Starting Pulse Watering...".format(i + 1, current_moisture))
                    start_time = utime.time()
                    
                    # While the soil is still drier than our target
                    while sensors[i].read() > STOP_WATERING:
                        # 1. Pulse the pump
                        pumps[i].value(0)
                        utime.sleep(PULSE_ON)
                        pumps[i].value(1) # Turn off immediately
                        
                        # 2. Wait for the 'Soak' (Let sensor catch up)
                        print("  Waiting for soak...")
                        lcd_show("P{}: PULSE DONE".format(i+1), "Soaking...")
                        utime.sleep(SOAK_TIME)
                        
                        # 3. Re-read and check safety
                        new_val = sensors[i].read()
                        print("  New Reading: {}".format(new_val))
                        
                        if (utime.time() - start_time) > MAX_SAFETY_TIME:
                            print("!! SAFETY TIMEOUT !!")
                            break
                    
                    print("Plant {} saturated. Final: {}".format(i + 1, sensors[i].read()))
                    lcd_show("P{}: SATURATED".format(i+1), "Val:{}".format(sensors[i].read()))

                else:
                    # Soil is within the healthy range or already wet
                    print("Plant {}: OK ({})".format(i + 1, current_moisture))
                    lcd_show("Plant {}: OK".format(i + 1), "Val:{}".format(current_moisture))
                    utime.sleep(1)

            print("--- Cycle complete. Waiting 5s ---")
            utime.sleep(5)

    except KeyboardInterrupt:
        for p in pumps:
            p.value(1)
        lcd_show("STOPPED", "All pumps OFF")
        print("Emergency Stop.")