
import time
from machine import UART, ADC, Pin
import os

soil = ADC(Pin(26))
 

# Calibration values:
# calibration = {
#     'air': 50000,
#     'arid': 40000,
#     'dry': 30000,
#     'saturated': 20000,
# }

AIR = 50000
ARID = 34000
DRY = 29000
SAT = 20000


def lin_interpolate(val, x, y, a, b):
    '''
    convert val between x and y to value between a and b
    '''
    return a + (b - a) * (val - x) / (y - x)


def scale(adc, upper_threshold=2000):
    if adc < SAT + upper_threshold:
        ## fully saturated == 1.0
        return 1.0
    elif adc < DRY + upper_threshold:
        ## saturated to dry, 1.0 to 0.3 
        return lin_interpolate(adc, SAT + upper_threshold, DRY + upper_threshold, 0.3, 1.0)
    elif adc < ARID + upper_threshold:
        ## dry to arid, 0.3 to 0.0 
        return lin_interpolate(adc, DRY + upper_threshold, ARID + upper_threshold, 0.0, 0.3)
    else:
        return -1


class DataWriter:

    def __init__(self, filename, max_size=1000000, overwrite=False) -> None:
        self.filename = filename
        self.max_size = max_size

        try:
            result = os.stat(filename)  # micropython `os` module does not have `path`
        except:
            print(f'{self.filename} does not exist')
            result = None
        if overwrite or result is None:
        # if not os.path.exists(filename) or overwrite:
            with open(self.filename, 'w') as f:
                f.write('')

    def write(self, line, verbose=False):
        if verbose: print(line)
        with open(self.filename, 'a') as f:
            line = str(line) + '\n'
            return f.write(line)


#Calibraton values
def read_moisture():
    adc_val = soil.read_u16()
    moisture = scale(adc_val)
    return moisture, adc_val


def calc_stats(stats, minmax=False):
    mean = sum(stats) / len(stats)
    std = (sum([(xi - mean)**2 for xi in stats]) / (len(stats) - 1)) ** 0.5
    if minmax: 
        minval, maxval = min(stats), max(stats)
        return mean, std, minval, maxval
    return mean, std


blue_led = Pin(13, Pin.OUT)
yellow_led = Pin(14, Pin.OUT)
red_led = Pin(15, Pin.OUT)

def indicate(moisture):
    if 0.3 < moisture <= 1.0:
        yellow_led.value(0)
        red_led.value(0)
        blue_led.value(1)
    elif 0. < moisture <= 0.3:
        blue_led.value(0)
        red_led.value(0)
        yellow_led.value(1)
    else:
        blue_led.value(0)
        yellow_led.value(0)
        red_led.value(1)


polling_rate = 5  # times per second
process_time = 0.01
sleep_time = 1.0 / polling_rate - process_time

print_period = 5  # seconds
polls_per_print = print_period * polling_rate

adcs = []
moistures = []
dw = DataWriter('data.txt', overwrite=True)

start_time = time.time()
count = 0
while True:
    count += 1
    moisture, adc = read_moisture()
    adcs.append(adc)
    moistures.append(moisture)
    if count % polls_per_print == 0:
        adc_stats = calc_stats(adcs)
        adcs = []
        moistures = []
        line = f'{time.time() - start_time},{",".join([str(_) for _ in adc_stats])}'
        dw.write(line, verbose=True)
    indicate(moisture)
    time.sleep(sleep_time)

# print('Readings completed. Stats:')
# print(calc_stats(adcs))
# print(' '.join(str(_) for _ in calc_stats(moistures)))

