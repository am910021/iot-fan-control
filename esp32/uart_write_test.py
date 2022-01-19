from machine import UART
from yuri.stream_lite import Stream
import time

uart = UART(2, baudrate=115200, tx=17, rx=16, txbuf=256, rxbuf=256)
stream = Stream()
stream.write_int(1226)
stream.write_byte(22)
uart.write(stream.get_bytes())

while True:
    time.sleep(0.5)
    buff = uart.read()
    if not buff or len(buff) < 4:
        continue

    istream = Stream(buff)
    if istream.read_int() != istream.length() or istream.read_int() != 1226:
        continue
    print(istream.read_str())
    break

