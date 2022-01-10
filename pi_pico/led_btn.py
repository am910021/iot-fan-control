from machine import Pin
import time, sys

ledb = Pin(25, Pin.OUT)
ledb.value(1)

led = Pin(15, Pin.OUT)
led.value(0)

rel = Pin(0, Pin.OUT)
rel.value(0)

button = Pin(14, Pin.IN, Pin.PULL_DOWN)

isChange = False
relVal = False

while True:
    if button.value():
        led.toggle()   #進行On/Off切換
        ledb.toggle()   #進行On/Off切換
        rel.toggle()
        time.sleep(0.5) #延遲0.5秒
        relVal = (not relVal)
        isChange = True
    
    if isChange:
        isChange = False
        status = "on" if relVal else "off"
        txt = "relay power %s"
        print(txt % status)
