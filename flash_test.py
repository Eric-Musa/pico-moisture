from machine import Pin
import time


red_led = Pin(15, Pin.OUT)
yellow_led = Pin(14, Pin.OUT)
blue_led = Pin(13, Pin.OUT)

def lightup(pin, duration=0.4, off=True):
    led = Pin(pin, Pin.OUT)
    if not off:
        led.value(1)
        time.sleep(duration)
    led.value(0)


while True:
    lightup(13, off=True)
    lightup(14, off=True)
    lightup(15, off=True)
    
