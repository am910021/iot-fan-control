# my_api.py
import gc
from yuri.http.response import Html
import time, sys
from yuri.stream_min import Stream

def get_uart_str(opcode):
    gc.collect()
    UART = getattr(__import__('machine'), 'UART')  # 動態載入UART模組
    Stream = getattr(getattr(__import__('yuri.stream_min'), 'stream_min'), 'Stream')  # 動態載入Stream模組
    uart = UART(2, baudrate=115200, tx=17, rx=16, rxbuf=1024, txbuf=1024)  # 開啟Uart
    ostream = Stream()  # 開啟串流
    ostream.write_int(1226)  # 寫入Uart的專屬編號
    ostream.write_byte(opcode)  # 寫入操作封包
    uart.write(ostream.get_bytes())  # 將串流資料寫入Uart，get_bytes=取得將串流資料+一組int長度的驗證資料
    ostream = None

    rt = []
    start = time.ticks_ms()
    timeout = 5  # timeout 秒單位
    # 如果讀取時間超過10秒，就停止讀取
    while (time.ticks_ms() - start) < timeout * 1000:
        istream = Stream(uart.read())  # 讀取Uart的資料，並創建Stream解析Uart的資料
        # 判斷istream資料大小是否足夠(第一判斷式、與第二判斷式)，判斷Uart的專屬編號(1226)是否正確
        if istream.length() < 8 or istream.read_int() != istream.length() or istream.read_int() != 1226:
            time.sleep(0.200)
            continue
        # 從串流封包頭取得str
        rt = parse_rtable(istream)
        istream = None
        break
    istream, ostream, Stream, uart, UART = None, None, None, None, None
    del sys.modules['yuri.stream_min']
    gc.collect()
    return rt


def update_rtable(opcode, arr):
    gc.collect()
    UART = getattr(__import__('machine'), 'UART')  # 動態載入UART模組
    Stream = getattr(getattr(__import__('yuri.stream_min'), 'stream_min'), 'Stream')  # 動態載入Stream模組
    uart = UART(2, baudrate=115200, tx=17, rx=16, txbuf=1024, rxbuf=1024)  # 開啟Uart
    ostream = Stream()  # 開啟串流
    ostream.write_int(1226)  # 寫入Uart的專屬編號
    ostream.write_byte(opcode)  # 寫入操作封包
    ostream.write_byte(len(arr))
    for i in range(len(arr)):
        for j in range(len(arr)):
            ostream.write_byte(arr[i][j])
    ostream.print_hex()
    uart.write(ostream.get_bytes())  # 將串流資料寫入Uart，get_bytes=取得將串流資料+一組int長度的驗證資料
    ostream = None

    status = 0
    start = time.ticks_ms()
    timeout = 5  # timeout 秒單位
    # 如果讀取時間超過10秒，就停止讀取
    while (time.ticks_ms() - start) < timeout * 1000:
        istream = Stream(uart.read())  # 讀取Uart的資料，並創建Stream解析Uart的資料
        # 判斷istream資料大小是否足夠(第一判斷式、與第二判斷式)，判斷Uart的專屬編號(1226)是否正確
        if istream.length() < 8 or istream.read_int() != istream.length() or istream.read_int() != 1226:
            time.sleep(0.200)
            continue
        # 從串流封包頭取得str
        status = istream.read_byte()
        istream = None
        break
    istream, ostream, Stream, uart, UART = None, None, None, None, None
    del sys.modules['yuri.stream_min']
    gc.collect()
    return status


def create_str_table(arr, head=True):
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
        rtable = request['body']['rtable']

        if len(rtable) == 0:
            return self.get_response(error='input R table is empty.')

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
    T = [[1, 2], [3, 4], [5, 6]]

    def get(self, request):
        info = {'title': 'Fan & Sensor Pair', 'table': FanSensorPair.create_str_table(FanSensorPair.T),
                'fst': FanSensorPair.create_str_table(FanSensorPair.T, False)}
        return Html.response('fan/info.html', info)

    @staticmethod
    def create_str_table(arr, head=True):
        ret = ""
        if head:
            ret = '      Sensor    Fan\r\n    |-------------\r\n'
        for i in range(len(arr)):
            if head:
                ret += '{0: >5}'.format(str(i + 1) + '|')
                ret += ', '.join(['{0: >6}'.format(e) for e in arr[i]]) + '\n'
            else:
                ret += ', '.join(['{0: >2}'.format(e) for e in arr[i]]) + '\n'
        return ret

