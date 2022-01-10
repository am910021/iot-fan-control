from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum
import sys

rels = [
    Pin(0, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(11, Pin.OUT),
    Pin(15, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(22, Pin.OUT),
    
    Pin(25, Pin.OUT)
    ]

for rel in rels:
    rel.value(0)