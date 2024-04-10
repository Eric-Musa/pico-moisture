import time
from machine import UART, ADC, Pin


soil = ADC(Pin(26))
 
#Calibraton values
def read_moisture(max_moisture_adc=19200, min_moisture_adc=50000):
# def read_moisture(max_moisture_adc=32000, min_moisture_adc=65535):
    adc_val = soil.read_u16()
    moisture = (min_moisture_adc-adc_val)*100/(min_moisture_adc-max_moisture_adc) 
 #    return {"moisture": moisture, "adc": adc_val, "timestamp": time.time()} 
    return moisture, adc_val, time.time()


count = 1
print_interval = 20
max_count = 100

adcs = []
moistures = []


def calc_stats(stats):
    mean = sum(stats) / len(stats)
    std = (sum([(xi - mean)**2 for xi in stats]) / (len(stats) - 1)) ** 0.5
    minval, maxval = min(stats), max(stats)
    return mean, std, minval, maxval


forever = False
while forever or count < max_count:
    time.sleep(0.05)
    count += 1
    if count % print_interval == 0:
        adc_stats = calc_stats(adcs)
        moisture_stats = calc_stats(moistures)
        
        if not forever: print(count / print_interval)
        print(adc_stats)
        print(moisture_stats)
        print()
        
        if forever:
            adcs = []
            moistures = []
            count = 0
    else:
        moisture, adc_val, timestamp = read_moisture()
        adcs.append(adc_val)
        moistures.append(moisture)

print('Readings completed. Stats:')
print(calc_stats(adcs))
print(' '.join(str(_) for _ in calc_stats(moistures)))

