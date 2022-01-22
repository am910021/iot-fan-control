# my_api.py
import gc
from yuri.http.response import Html
import time, sys
from yuri.stream_min import Stream


def create_OStream(opcode) -> Stream:
    ostream = Stream()  # 開啟串流
    ostream.write_int(1226)  # 寫入Uart的專屬編號
    ostream.write_byte(opcode)  # 寫入操作封包
    return ostream


def uart_send(ostream: Stream) -> Stream:
    gc.collect()
    uart = getattr(__import__('machine'), 'UART')(2, baudrate=115200, tx=17, rx=16, rxbuf=1024, txbuf=1024)  # 開啟Uart
    uart.write(ostream.get_bytes())  # 將串流資料寫入Uart，get_bytes=取得將串流資料+一組int長度的驗證資料

    rstream = None
    start = time.ticks_ms()
    timeout = 5  # timeout 秒單位
    # 如果讀取時間超過10秒，就停止讀取
    while (time.ticks_ms() - start) < timeout * 1000:
        istream = Stream(uart.read())  # 讀取Uart的資料，並創建Stream解析Uart的資料
        # 判斷istream資料大小是否足夠(第一判斷式、與第二判斷式)，判斷Uart的專屬編號(1226)是否正確
        if istream.length() < 8 or istream.read_int() != istream.length() or istream.read_int() != 1226:
            time.sleep(0.200)
            continue
        rstream = istream
        break

    uart = None
    gc.collect()
    return rstream


def get_uart_str(opcode):
    gc.collect()
    ostream = create_OStream(opcode)
    return parse_rtable(uart_send(ostream))


def update_rtable(opcode, arr):
    gc.collect()
    ostream = create_OStream(opcode)
    ostream.write_byte(len(arr))
    for i in range(len(arr)):
        for j in range(len(arr)):
            ostream.write_byte(arr[i][j])
    istream = uart_send(ostream)

    return istream.read_byte()


def create_str_table(arr, head=True):
    if len(arr) == 0:
        return ""

    ret = ""
    if head:
        ret = '    ' + '  '.join(['{0: >3}'.format(e + 1) for e in range(len(arr))]) + '\n'
        ret += '   |' + '-'.join(['----' for e in range(len(arr))]) + '\n'
    for i in range(len(arr)):
        if head:
            ret += '{0: >4}'.format(str(i + 1) + '|')
        ret += ', '.join(['{0: >3}'.format(e) for e in arr[i]]) + '\n'
    return ret


def parse_rtable(stream):
    size = stream.read_byte()
    rt = []
    for i in range(size):
        tmp = []
        for j in range(size):
            tmp.append(stream.read_byte())
        rt.append(tmp)
    return rt


class RTable:
    def get(self, request):
        return self.get_response()

    def post(self, request):
        if 'rtable' not in request['body'] or len(request['body']['rtable']) == 0:
            return self.get_response(error='input R table is empty.')

        rtable = request['body']['rtable']
        rtable = rtable[:-6] if rtable[-6:] == '%0D%0A' else rtable
        rst = rtable.replace('%2C', ',').replace('+', '').split('%0D%0A')
        print()
        rtable = None
        rt = []
        for i in rst:
            tmp = []
            tmp2 = i.split(',')
            if len(tmp2) != len(rst):
                print(len(tmp2), len(rst))
                return self.get_response(error='Incorrect R table value entered.')
            for j in tmp2:
                tmp.append(int(j))
            rt.append(tmp)
        print(rt)
        status = update_rtable(32, rt)
        if status != len(rst):
            return self.get_response(error='remote save R Table failed.')

        return self.get_response(success='The R table update is complete, and the Q table update takes a while.')

    def get_response(self, arr=[], error="", success=""):
        rt = get_uart_str(12)
        info = {'title': 'R Table info', 'name': 'R', 'rti': create_str_table(rt),
                'rt': create_str_table(rt, False), 'error': error, 'success': success}
        return Html.response('fan/table/edit.html', info)


class QTable:
    def get(self, request):
        qt = get_uart_str(13)
        info = {'title': 'Q Table info', 'name': 'Q', 'tb': create_str_table(qt)}
        return Html.response('fan/table/info.html', info)


class FanSensorPair:

    def get(self, request):
        return FanSensorPair.get_response()

    def post(self, request):
        table = request['body']['table']

        if len(table) == 0:
            return FanSensorPair.get_response(error='input table is empty.')

        table = table[:-6] if table[-6:] == '%0D%0A' else table
        rst = table.replace('%2C', ',').replace('+', '').split('%0D%0A')
        ttable = []
        for i in rst:
            tmp = i.split(',')
            if len(tmp) != 2:
                return FanSensorPair.get_response(error='Incorrect table value entered.')
            ttable.append([int(tmp[0]), int(tmp[1])])

        print(ttable)
        if not self.update_fs_pair(ttable):
            return FanSensorPair.get_response(error='remote save Fan&Sensor Table failed.')

        return FanSensorPair.get_response(success='The Fan&Sensor table update is complete.')

    def update_fs_pair(self, ttable):
        ostream = create_OStream(50)
        ostream.write_byte(len(ttable))
        for i in ttable:
            ostream.write_byte(i[0])
            ostream.write_byte(i[1])
        status = uart_send(ostream).read_byte()
        return status == len(ttable)

    @staticmethod
    def get_response(arr=[], error="", success=""):
        istream = uart_send(create_OStream(51))
        istream.print_hex()
        rt = []
        size = istream.read_byte()
        for i in range(size):
            tmp = [-1, -1]
            tmp[0], tmp[1] = istream.read_byte(), istream.read_byte()
            rt.append(tmp)

        info = {'title': 'Fan & Sensor Pair', 'table': FanSensorPair.create_str_table(rt),
                'fst': FanSensorPair.create_str_table(rt, False), 'error': error, 'success': success}
        gc.collect()
        return Html.response('fan/info.html', info)

    @staticmethod
    def create_str_table(arr, head=True):
        ret = ""
        if head:
            ret = '        Fan  Sensor\r\n    |--------------\r\n'
        for i in range(len(arr)):
            if head:
                ret += '{0: >5}'.format(str(i + 1) + '|')
                ret += ','.join(['{0: >6}'.format(e) for e in arr[i]]) + '\n'
            else:
                ret += ','.join(['{0: >2}'.format(e) for e in arr[i]]) + '\n'
        return ret
