from machine import UART, Pin
from yuri.stream import Stream
class UartWrite:
    _instance = None
    _UART_ID = 8204

    @staticmethod
    def get_instance():
        if UartWrite._instance is None:
            UartWrite()
        return UartWrite._instance

    def __init__(self):
        if UartWrite._instance is not None:
            pass
            #raise Exception('only one instance can exist')
        else:
            self._id = id(self)
            UartWrite._instance = self
            self._uart = UART(1, baudrate=115200)
    
    def get_id(self):
        return self._id
    
    def write(self, b:bytes):
        stream = Stream()
        stream.writeShort(UartWrite._UART_ID)
        stream.write(b)
        self._uart.write(stream.getBytes())
        
uart = UartWrite.get_instance()