from machine import UART
from yuri.stream_full import Stream
import time

UART_Tx_BUFFER_LENGTH = 256
UART_Rx_BUFFER_LENGTH = 256


class UartTest:
    def __init__(self, uartPort=2, baudRate=115200, txPin=(17), rxPin=(16)):
        self.__uartPort = uartPort
        self.__baudRate = baudRate
        self.__txPin = txPin
        self.__rxPin = rxPin
        # print(self.__uartPort,       self.__baudRate,        self.__txPin,        self.__rxPin)
        self.__uartObj = UART(self.__uartPort, baudrate=self.__baudRate, tx=self.__txPin, rx=self.__rxPin,
                              txbuf=UART_Tx_BUFFER_LENGTH, rxbuf=UART_Rx_BUFFER_LENGTH)

    def run(self):
        stream = Stream()
        stream.write_short(1226)
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
