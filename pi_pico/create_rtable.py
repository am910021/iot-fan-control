from machine import UART, Pin
from yuri.stream_full import Stream
import time


def tw():
    R = [
        [-1, -1, -1, -1, 0, -1],
        [-1, -1, -1, 0, -1, 100],
        [-1, -1, -1, 0, -1, -1],
        [-1, 0, 0, -1, 0, -1],
        [0, -1, -1, 0, -1, 100],
        [-1, 0, -1, -1, 0, 100]
    ]
    stream = Stream()
    stream.write_byte(len(R))
    for i in R:
        for j in i:
            stream.write_byte(j)

    with open('r.table', 'wb') as f:
        f.write(stream.get_bytes())


def tr():
    # Stream = getattr(getattr(__import__('yuri.stream_lite'), 'stream_lite'), 'Stream')
    R = None
    with open('r.table', 'rb') as f:
        stream = Stream(f.read())
        size = stream.read_byte()
        R = [[0] * size] * size
        for i in range(size):
            for j in range(size):
                R[i][j] = stream.read_byte()
    return R


def handler():
    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(0), txbuf=256, rxbuf=256)
    while True:
        time.sleep(0.5)
        buff = uart.read()
        if not buff or len(buff) < 4:
            continue

        istream = Stream(buff)
        if istream.read_int() != 1226:
            continue

        op = istream.read_byte()
        print('recv op code {}'.format(op))
        ostream = Stream()
        if op == 22:
            R = tr()
            b = '    ' + '  '.join(['{0: >3}'.format(e + 1) for e in range(len(R))]) + '\n'
            b += '   |' + '-'.join(['----' for e in range(len(R))]) + '\n'
            for i in range(len(R)):
                b += '{0: >4}'.format(str(i + 1) + '|')
                b += ', '.join(['{0: >3}'.format(e) for e in R[i]]) + '\n'
            uart.write(ostream.get_bytes())
        elif op == 12:
            rs = istream.read_str()
            rs = rs.replace(' ', '')
            rst = rs.split('\r\n')
            print(rst)
        else:
            print('unknown op code {}'.format(op))


tw()
tr()
handler()