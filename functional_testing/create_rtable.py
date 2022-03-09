import gc, sys, os
from machine import UART, Pin
from yuri.stream_min import Stream
import time, math
import _thread


class Status:
    learn_running = False

    UART_SERIAL = 1226


def exists(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False


def create_out_stream() -> Stream:
    ostream = Stream()  # 開啟串流
    ostream.write_int(1226)  # 寫入Uart的專屬編號
    return ostream


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
        with open('/tmp/q.table', 'wb') as f:
            f.write(stream.get_bytes())


def read_file(path) -> Stream:
    stream = None
    if not exists(path):
        return None

    with open(path, 'rb') as f:
        stream = Stream(f.read())
        stream.read_int()  # size check
        f.close()
    return stream


def read_table(name):
    stream = read_file('/tmp/' + name + '.table')
    if not stream:
        return []

    size = stream.read_byte()
    table = []
    for i in range(size):
        tmp = []
        for j in range(size):
            buff = stream.read_byte()
            tmp.append(buff)
        table.append(tmp)
    return table


def create_str_table(name):
    table = read_table(name)
    ret = '    ' + '  '.join(['{0: >3}'.format(e + 1) for e in range(len(table))]) + '\n'
    ret += '   |' + '-'.join(['----' for e in range(len(table))]) + '\n'
    for i in range(len(table)):
        ret += '{0: >4}'.format(str(i + 1) + '|')
        ret += ', '.join(['{0: >3}'.format(e) for e in table[i]]) + '\n'
    return ret


def uart_handler(uart):
    istream = Stream(uart.read())  # 讀取Uart的資料，並創建Stream
    # 判斷istream資料大小是否足夠，判斷Uart的專屬編號(Status.UART_SERIAL)是否正確
    if istream.length() < 8 or istream.read_int() != istream.length() or istream.read_int() != Status.UART_SERIAL:
        return

    op = istream.read_byte()
    print('recv op code {}'.format(op))

    # 處理前的R table
    if op == 12:
        rt = read_table('r')
        ostream = create_out_stream()
        ostream.write_byte(len(rt))
        for i in range(len(rt)):
            for j in range(len(rt)):
                ostream.write_byte(rt[i][j])
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    # 處理前的Q table
    elif op == 13:
        rt = read_table('q')
        ostream = create_out_stream()
        ostream.write_byte(len(rt))
        for i in range(len(rt)):
            for j in range(len(rt)):
                ostream.write_byte(rt[i][j])
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    # 處理後的R table
    elif op == 22:
        ostream = create_out_stream()
        ostream.write_str(create_str_table('r'))
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    # 處理後的Q table
    elif op == 23:
        ostream = create_out_stream()
        ostream.write_str(create_str_table('q'))
        ostream.print_hex()
        uart.write(ostream.get_bytes())
    # 儲存R table
    elif op == 32:
        fstream = Stream(istream.get_bytes(True))
        with open('/tmp/r.table', 'wb') as f:
            print(fstream.length())
            fstream.print_hex()
            f.write(fstream.get_bytes())
            f.close()
        ostream = create_out_stream()
        ostream.write_byte(fstream.read_byte())
        ostream.print_hex()
        uart.write(ostream.get_bytes())
        Status.learn_running = True
    #  計算Q table
    elif op == 43:
        Status.learn_running = True
    #  寫入fs.table
    elif op == 50:
        rt = []
        istream.print_hex()
        fstream = Stream(istream.get_bytes(True))
        size = istream.read_byte()
        try:
            for i in range(size):
                tmp = [-1, -1, 50, 50]
                tmp[0], tmp[1] = istream.read_byte(), istream.read_byte()
                tmp[2], tmp[3] = istream.read_byte(), istream.read_byte()
                Pin(tmp[0], Pin.OUT)
                Pin(tmp[1], Pin.OUT, Pin.PULL_DOWN)
                if tmp[2] < 0 or tmp[2] > 100 or tmp[3] < 0 or tmp[3] > 100:
                    ostream = create_out_stream()
                    ostream.write_byte(-2)
                    print('temperature err')
                    uart.write(ostream.get_bytes())
                    return
                rt.append(tmp)
        except:
            print('except err')
            ostream = create_out_stream()
            ostream.write_byte(-1)
            uart.write(ostream.get_bytes())
            return

        with open('/tmp/fs.table', 'wb') as f:
            print(fstream.length())
            fstream.print_hex()
            f.write(fstream.get_bytes())
            f.close()

        ostream = create_out_stream()
        ostream.write_byte(len(rt))
        ostream.print_hex()
        print('no err')
        uart.write(ostream.get_bytes())
    #  讀取fs.table
    elif op == 51:
        ostream = create_out_stream()
        fstream = read_file('/tmp/fs.table')
        if not fstream:
            ostream.write_byte(-1)
            return
        fstream.print_hex()
        ostream.write(fstream.get_bytes(True))
        uart.write(ostream.get_bytes())

    elif op == 127:
        status = 0
        if exists('/tmp/fs.table'):
            os.remove('/tmp/fs.table')
            create_blank_fs_table()
            status += 1
        if exists('/tmp/r.table'):
            os.remove('/tmp/r.table')
            data = [[-1 for x in range(6)] for y in range(6)]
            create_blank_table_with('r', data)
            status += 2
        if exists('/tmp/q.table'):
            os.remove('/tmp/q.table')
            data = [[0 for x in range(6)] for y in range(6)]
            create_blank_table_with('q', data)
            status += 4
        ostream = create_out_stream()
        ostream.write_byte(status)
        uart.write(ostream.get_bytes())
    else:
        print('unknown op code {}'.format(op))


def run_learning():
    if Status.learn_running:
        print('Learning start')
        learn = Learning(read_table('r'), 0.8)
        learn.learn_for_time(1000)
        learn.write_qtable()
        Status.learn_running = False


def second_thread():
    while True:
        try:
            gc.collect()
            run_learning()
        except Exception as e:
            sys.print_exception(e)
        finally:
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
            time.sleep(0.25)
    except Exception as e:
        sys.print_exception(e)


def create_blank_fs_table():
    table = [[22, 21, 50, 50], [19, 20, 50, 50]]
    fstream = Stream()
    fstream.write_byte(len(table))
    for i in table:
        fstream.write_byte(i[0])
        fstream.write_byte(i[1])
        fstream.write_byte(i[2])
        fstream.write_byte(i[3])
    with open('/tmp/fs.table', 'wb') as f:
        f.write(fstream.get_bytes())


def create_blank_table_with(name, data):
    fstream = Stream()
    fstream.write_byte(len(data))
    for i in data:
        for j in i:
            fstream.write_byte(j)
    with open('/tmp/' + name + '.table', 'wb') as f:
        f.write(fstream.get_bytes())


if __name__ == '__main__':
    start = time.ticks_ms()
    countdown = 5
    while (time.ticks_ms() - start) < (countdown * 1000):
        print('Execute Uart Handler program after %d seconds.' % (countdown - round((time.ticks_ms() - start) / 1000)))
        time.sleep(1)

    if not exists('/tmp'):
        os.mkdir('/tmp')
    if not exists('/tmp/fs.table'):
        create_blank_fs_table()
    if not exists('/tmp/r.table'):
        arr = [[-1 for x in range(6)] for y in range(6)]
        create_blank_table_with('r', arr)
    if not exists('/tmp/q.table'):
        arr = [[0 for x in range(6)] for y in range(6)]
        create_blank_table_with('q', arr)
    Status.learn_running = True
    _thread.start_new_thread(second_thread, ())
    time.sleep(0.5)
    handler()

