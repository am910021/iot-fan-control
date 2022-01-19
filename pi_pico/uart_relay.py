from machine import UART, Pin, I2C
from yuri.stream import Stream
from yuri.timer import Timer
from yuri.uart_reader import uart
import time
import sys

rels = [
    Pin(0, Pin.OUT),
    Pin(4, Pin.OUT),
    Pin(11, Pin.OUT),
    Pin(15, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(22, Pin.OUT),
    
    Pin(25, Pin.OUT),
    ]

def control():
    time.sleep(100/1000)
        
    if not uart.is_available():
        return
        
    stream = uart.get_stream()
    stream.print_hex()
        
if __name__ == '__main__':
    for rel in rels:
        rel.value(0)

    while True:
        control()
        
        
        
        
        
        
