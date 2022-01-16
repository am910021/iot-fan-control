from machine import UART, Pin
from yuri.stream import Stream
import gc

class UartReader:
    _instance = None
    _UART_ID = 8204

    @staticmethod
    def get_instance():
        if UartReader._instance is None:
            UartReader()
        return UartReader._instance

    def __init__(self):
        if UartReader._instance is not None:
            pass
            #raise Exception('only one instance can exist')
        else:
            self._id = id(self)
            UartReader._instance = self
            self._uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9), txbuf=1024, rxbuf=1024)
            self._stream=None
    
    def get_id(self):
        return self._id
    
    def isAvailable(self):
        self._stream=None
        buff = self._uart.read()
        if not buff or len(buff) < 2:
            return False
        stream = Stream(buff)
        uart_id = stream.read_short()
        if uart_id != UartReader._UART_ID:
            return False
        
        self._stream = stream
        return True
        
    
    def getStream(self) -> Stream:
        stream = self._stream
        gc.collect()
        return stream
        
uart = UartReader.get_instance()
