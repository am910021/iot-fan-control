from machine import Pin, I2C
import time, sys
from dht import DHT11, InvalidChecksum


ledb = Pin(25, Pin.OUT)
ledb.value(1)

led = Pin(15, Pin.OUT)
led.value(0)

rel = Pin(0, Pin.OUT)
rel.value(0)

button = Pin(14, Pin.IN, Pin.PULL_UP)


isChange = False
relVal = False
isRunning = False

while True:
  
        #led.toggle()   #進行On/Off切換
        #ledb.toggle()   #進行On/Off切換
        #rel.toggle()
        #
        #relVal = (not relVal)
        #isChange = True
        
    if isRunning:
        try:
            pin = Pin(28, Pin.OUT, Pin.PULL_DOWN)
            sensor = DHT11(pin)
            t  = (sensor.temperature)
            h = (sensor.humidity)
            print("Temperature: {}".format(sensor.temperature))
            print("Humidity: {}".format(sensor.humidity))
            time.sleep(0.5) #延遲0.5秒
        except:
            print()
    
    if isChange:
        isChange = False
        status = "on" if relVal else "off"
        txt = "relay power %s"
        print(txt % status)

def button_handler(pin):
    global isRunning
    isRunning = (not isRunning)
    status = "on" if isRunning else "off"
    txt = "dht detector turn %s"
    print(txt % status) 


button.irq(trigger = Pin.IRQ_RISING, handler = button_handler)
