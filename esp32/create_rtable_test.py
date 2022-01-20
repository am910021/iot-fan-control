from machine import UART, Pin
from yuri.stream_min import Stream
import time, math


class Learning:
    def __init__(self, rtable, rate=0.8):
        self.STATE = ['A', 'B', 'C', 'D', 'E', 'F']
        self._rate = rate
        self._rtable = rtable
        self._w = len(self._rtable)
        self._qtable = [[0 for x in range(self._w)] for y in range(self._w)]

    def learn(self):
        room_score = -1
        for state in range(len(self._rtable)):
            for action in range(len(self._rtable)):
                room_score = self._rtable[state][action]
                if room_score == -1:
                    continue

                qMax = max(self._qtable[action])
                self._qtable[state][action] = self._rtable[state][action] + self._rate * qMax

    def learn_for_time(self, times):
        self._qtable = [[0 for x in range(self._w)] for y in range(self._w)]
        start_time = time.ticks_ms()
        for i in range(times):
            self.learn()
        end_time = time.ticks_ms()
        print("The total learning time is %f milliseconds." % (end_time - start_time))
        qMax = max(map(max, self._qtable))
        for i in range(len(self._qtable)):
            for j in range(len(self._qtable)):
                self._qtable[i][j] = round((self._qtable[i][j] / qMax) * 100)

    def print_q(self):
        for i in self._qtable:
            print(i)

    def write_qtable(self):
        stream = Stream()
        stream.write_short(len(self._qtable))
        for i in self._qtable:
            for j in i:
                stream.write_short(round(j))
        with open('q.table', 'wb') as f:
            f.write(stream.get_bytes())


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
    stream.write_short(len(R))
    for i in R:
        for j in i:
            stream.write_short(j)
    with open('r.table', 'wb') as f:
        print(stream.length())
        stream.print_hex()
        f.write(stream.get_bytes())
    return R


def read_table(name):
    T = None
    with open(name + '.table', 'rb') as f:
        stream = Stream(f.read())
        stream.read_int()  # size check
        size = stream.read_short()
        T = []
        for i in range(size):
            tmp = []
            for j in range(size):
                buff = stream.read_short()
                tmp.append(buff)
            T.append(tmp)
    return T


def create_str_table(name):
    T = read_table(name)
    ret = '    ' + '  '.join(['{0: >3}'.format(e + 1) for e in range(len(T))]) + '\n'
    ret += '   |' + '-'.join(['----' for e in range(len(T))]) + '\n'
    for i in range(len(T)):
        ret += '{0: >4}'.format(str(i + 1) + '|')
        ret += ', '.join(['{0: >3}'.format(e) for e in T[i]]) + '\n'
    return ret


def uart_handler(uart):
    istream = Stream(uart.read())  # 讀取Uart的資料，並創建Stream
    # 判斷istream資料大小是否足夠，判斷Uart的專屬編號(1226)是否正確
    if istream.length() < 8 or istream.read_int() != istream.length() or istream.read_int() != 1226:
        time.sleep(0.200)
        return

    op = istream.read_byte()
    print('recv op code {}'.format(op))

    if op == 2:
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_str(create_str_table('r'))
        ostream.write_str(create_str_table('q'))
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    elif op == 22:
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_str(create_str_table('r'))
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    elif op == 23:
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_str(create_str_table('q'))
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    elif op == 12:
        rs = istream.read_str()
        rs = rs.replace(' ', '')
        rst = rs.split('\r\n')
        print(rst)
    else:
        print('unknown op code {}'.format(op))


def handler():
    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1), txbuf=256, rxbuf=256)
    uart2 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), txbuf=256, rxbuf=256)
    while True:
        uart_handler(uart)
        uart_handler(uart2)


tw()
learn = Learning(read_table('r'), 0.8)
learn.learn_for_time(1000)
learn.write_qtable()
handler()

