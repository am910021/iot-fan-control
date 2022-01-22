import gc, sys, os
from machine import UART, Pin
from yuri.stream_min import Stream
import time, math
import _thread


class Status:
    learn_running = False

def exists(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False


class Learning:
    def __init__(self, rtable, rate=0.8):
        self.STATE = ['A', 'B', 'C', 'D', 'E', 'F']
        self._rate = rate
        self._rtable = rtable
        self._w = len(self._rtable)
        self._qtable = [[0 for x in range(self._w)] for y in range(self._w)]

    def learn(self):
        gc.collect()
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
        print()
        end_time = time.ticks_ms()
        print("The total learning time is %f milliseconds." % (end_time - start_time))
        qMax = max(map(max, self._qtable))
        if qMax <= 0:
            return
        for i in range(len(self._qtable)):
            for j in range(len(self._qtable)):
                self._qtable[i][j] = round((self._qtable[i][j] / qMax) * 100)

    def print_q(self):
        for i in self._qtable:
            print(i)

    def write_qtable(self):
        stream = Stream()
        stream.write_byte(len(self._qtable))
        for i in self._qtable:
            for j in i:
                stream.write_byte(round(j))
        with open('q.table', 'wb') as f:
            f.write(stream.get_bytes())


def tw():
    R = [
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1]
    ]

    R2 = [
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
        stream.print_hex()
        f.write(stream.get_bytes())
    return R


def read_file(path) -> Stream:
    stream = None
    with open(path, 'rb') as f:
        stream = Stream(f.read())
        stream.read_int()  # size check
        f.close()
    return stream


def read_table(name):
    stream = read_file(name + '.table')
    if not stream:
        return []

    stream.read_int()  # size check
    size = stream.read_byte()
    T = []
    for i in range(size):
        tmp = []
        for j in range(size):
            buff = stream.read_byte()
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
        return

    op = istream.read_byte()
    print('recv op code {}'.format(op))

    # 處理前的R table
    if op == 12:
        rt = read_table('r')
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_byte(len(rt))
        for i in range(len(rt)):
            for j in range(len(rt)):
                ostream.write_byte(rt[i][j])
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    # 處理前的Q table
    elif op == 13:
        rt = read_table('q')
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_byte(len(rt))
        for i in range(len(rt)):
            for j in range(len(rt)):
                ostream.write_byte(rt[i][j])
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    # 處理後的R table
    elif op == 22:
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_str(create_str_table('r'))
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    # 處理後的Q table
    elif op == 23:
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_str(create_str_table('q'))
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    # 儲存R table
    elif op == 32:
        fstream = Stream(istream.get_bytes(True))
        with open('r.table', 'wb') as f:
            print(fstream.length())
            fstream.print_hex()
            f.write(fstream.get_bytes())
            f.close()
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_byte(fstream.read_byte())
        ostream.print_hex()
        uart.write(ostream.get_bytes())
        Status.learn_running = True
    #  計算Q table
    elif op == 43:
        Status.learn_running = True
    elif op == 50:
        fstream = Stream(istream.get_bytes(True))
        with open('fs.table', 'wb') as f:
            print(fstream.length())
            fstream.print_hex()
            f.write(fstream.get_bytes())
            f.close()
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_byte(fstream.read_byte())
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    elif op==51:
        ostream = Stream()
        ostream.write_int(1226)
        fstream = read_file('fs.table')
        if not fstream:
            ostream.write_byte(-1)
        fstream.print_hex()
        ostream.write(fstream.get_bytes(True))
        uart.write(ostream.get_bytes())

    elif op == 99:
        ostream = Stream()
        ostream.write_int(1226)
        ostream.write_str(istream.read_str())
        ostream.print_hex()
        uart.write(ostream.get_bytes())

    else:
        print('unknown op code {}'.format(op))


def thread_learning():
    while True:
        gc.collect()
        if Status.learn_running:
            time.sleep(0.5)
            print('Learning start')
            learn = Learning(read_table('r'), 0.8)
            learn.learn_for_time(1000)
            learn.write_qtable()
            Status.learn_running = False
        time.sleep(0.5)



def handler():
    print('Uart handler start')
    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1), txbuf=1024, rxbuf=1024)
    uart2 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), txbuf=1024, rxbuf=1024)
    try:
        while True:
            gc.collect()
            uart_handler(uart)
            uart_handler(uart2)
            time.sleep(0.5)
    except Exception as e:
        sys.print_exception(e)




if __name__ == '__main__':
    start = time.ticks_ms()
    countdown = 5
    while (time.ticks_ms() - start) < (countdown * 1000):
        print('Execute Uart Handler program after %d seconds.' % (countdown - round((time.ticks_ms() - start) / 1000)))
        time.sleep(1)

    tw()
    Status.learn_running = True
    _thread.start_new_thread(thread_learning, ())
    handler()



