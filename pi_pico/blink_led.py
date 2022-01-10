from machine import Pin, Timer
import time
led = Pin(25, Pin.OUT)
led2 = Pin(15, Pin.OUT)

led.value(0)
led2.value(0)
led2.value(1)

tim = Timer()
def tick(timer):
    global led
    led.toggle()
#tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
while True:
    time.sleep(1)
    led.toggle()
    led2.toggle()