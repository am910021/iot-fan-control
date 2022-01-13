from machine import UART, Pin
from yuri.stream import Stream
import time
import gc

UART_Tx_BUFFER_LENGTH = 1024
UART_Rx_BUFFER_LENGTH = 1024


class UartTest:
    def __init__(self, uartPort=1, baudRate=115200):
        self.__uartPort = uartPort
        self.__baudRate = baudRate
        self.__uartObj = UART(self.__uartPort, baudrate=self.__baudRate)

    def run(self):
        now = time.time()
        stream = Stream()
        stream.writeByte(20)
        stream.writeLong(time.ticks_ms())
        stream.printHex()
        self.__uartObj.write(stream.getBytes())



    def close(self):
        self.__uartObj.deinit()


if __name__ == '__main__':
    gc.collect()
    test = UartTest()
    while True:
        test.run()
        time.sleep(500 / 1000)
