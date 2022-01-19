from machine import UART
from yuri.stream_lite import Stream
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
            # raise Exception('only one instance can exist')
        else:
            self._id = id(self)
            UartReader._instance = self
            self._uart = UART(1, baudrate=115200, tx=33, rx=32, txbuf=256, rxbuf=256)
            self._stream = None

    def get_id(self):
        return self._id

    def is_available(self):
        self._stream = None
        buff = self._uart.read()
        if not buff or len(buff) < 2:
            return False
        stream = Stream(buff)
        uart_id = stream.read_int()
        if uart_id != UartReader._UART_ID:
            return False

        self._stream = stream
        return True

    def get_stream(self) -> Stream:
        stream = self._stream
        gc.collect()
        return stream


uart = UartReader.get_instance()
