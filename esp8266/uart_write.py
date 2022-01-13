from machine import UART, Pin

class UartWrite:
    # 加底線表示為私有變數
    _instance = None

    @staticmethod
    def get_instance():
        if UartWrite._instance is None:
            UartWrite()
        return UartWrite._instance
    # 此處應為私有的建構子
    def __init__(self):
        if UartWrite._instance is not None:
            raise Exception('only one instance can exist')
        else:
            self._id = id(self)
            UartWrite._instance = self
            self._uart = UART(1, baudrate=115200)
    
    def get_id(self):
        return self._id
    
    def write(b:bytes):
        self._uart.write(b)