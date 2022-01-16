from machine import UART, Pin
from yuri.stream import Stream
import time

UART_Tx_BUFFER_LENGTH = 1024
UART_Rx_BUFFER_LENGTH = 1024


class UartTest:
    def __init__(self, uartPort=1, baudRate=115200, txPin=(8), rxPin=(9)):
        self.__uartPort = uartPort
        self.__baudRate = baudRate
        self.__txPin = txPin
        self.__rxPin = rxPin
        # print(self.__uartPort,       self.__baudRate,        self.__txPin,        self.__rxPin)
        self.__uartObj = UART(self.__uartPort, baudrate=self.__baudRate, tx=Pin(self.__txPin), rx=Pin(self.__rxPin),
                              txbuf=UART_Tx_BUFFER_LENGTH, rxbuf=UART_Rx_BUFFER_LENGTH)

    def run(self):
        stream = Stream()
        stream.write_byte(20)
        stream.write_int(time.time())
        stream.print_hex()
        self.__uartObj.write(stream.get_bytes())



    def close(self):
        self.__uartObj.deinit()


if __name__ == '__main__':
    test = UartTest()
    while True:
        test.run()
        time.sleep(500 / 1000)
