from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum
import sys

rel = Pin(0, Pin.OUT)
rel.value(0)

rel2 = Pin(6, Pin.OUT)
rel2.value(0)

led = Pin(1, Pin.OUT)
led.value(0)

isRunning=False
t,h =0,0
pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)

while True:
    time.sleep(0.5)

    try:
        sensor = DHT11(pin)
        t  = (sensor.temperature)
        h = (sensor.humidity)
    except:
        pass
    print("Temperature: {:.2f}".format(t))
    print("   Humidity: {:.2f}".format(h))
    
    if (h > 75.0) and (not isRunning):
        rel.toggle()
        rel2.toggle()
        led.toggle()
        isRunning = True
        
    if (h < 70.0) and isRunning:
        rel.toggle()
        rel2.toggle()
        led.toggle()
        isRunning = False
    
    
    
