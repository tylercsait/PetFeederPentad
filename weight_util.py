import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
from collections import Counter

GPIO.setwarnings(False)

# Initialize HX711
def init_weight_sensor():
    hx = HX711(dout=24, pd_sck=23)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(386)
    hx.reset()
    hx.tare()
    print("Tare done! Add weight now...")
    return hx

def get_weight(hx):
    bin_width = 0.2
    batch_size = 5
    num_batches = 5
    mode_values = []

    for _ in range(num_batches):
        readings = []
        for _ in range(batch_size):
            val = hx.get_weight(1)
            readings.append(val)
            time.sleep(0.01)

        bin_indices = [round(reading / bin_width) for reading in readings]
        bin_counts = Counter(bin_indices)
        mode_bin_index = max(bin_counts, key=bin_counts.get)
        mode_value = mode_bin_index * bin_width
        mode_values.append(mode_value)
        time.sleep(0.05)

    mode_counter = Counter(mode_values)
    final_mode_data = mode_counter.most_common(1)
    if final_mode_data:
        return final_mode_data[0][0]
    else:
        return None

def cleanup():
    GPIO.cleanup()
    sys.exit()

GRAMS_PER_PORTION = 17

def grams_to_portions(grams):
    portions = grams/GRAMS_PER_PORTION
    return portions

