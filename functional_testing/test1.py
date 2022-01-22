from machine import UART
from yuri.stream_min import Stream
import time, sys

def get_uart_str(opcode):
    gc.collect()
    UART = getattr(__import__('machine'), 'UART')  # 動態載入UART模組
    Stream = getattr(getattr(__import__('yuri.stream_min'), 'stream_min'), 'Stream')  # 動態載入Stream模組
    uart = UART(2, baudrate=115200, tx=17, rx=16)  # 開啟Uart
    ostream = Stream()  # 開啟串流
    ostream.write_int(1226)  # 寫入Uart的專屬編號
    ostream.write_byte(opcode)  # 寫入操作封包
    uart.write(ostream.get_bytes())  # 將串流資料寫入Uart，get_bytes=取得將串流資料+一組int長度的驗證資料
    ostream = None

    string = None
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
        string = istream.read_str()
        istream = None
        break
    istream, ostream, Stream, uart, UART = None, None, None, None, None
    del sys.modules['yuri.stream_min']
    gc.collect()
    return string

name="test1.txt"
uart = UART(2, baudrate=115200, tx=17, rx=16, txbuf=1024, rxbuf=1024)
ostream = Stream()  # 開啟串流
ostream.write_int(1226)
ostream.write_byte(99)
ostream.write_str(name)
string=""
arr=[64,128,256,512,1024]
for i in range((32-5)-len(name)):
    string+="A"
ostream.write_str(string)
uart.write(ostream.get_bytes())



#print(get_uart_str(22))
