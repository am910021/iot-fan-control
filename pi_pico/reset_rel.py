from machine import Pin, I2C
import utime as time
from dht import DHT11, InvalidChecksum
import sys

rels = [
    Pin(6, Pin.OUT),
    Pin(8, Pin.OUT),
    Pin(10, Pin.OUT),
    Pin(12, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(17, Pin.OUT),
    
    Pin(25, Pin.OUT)
    ]

for rel in rels:
    rel.value(0)