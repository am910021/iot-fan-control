from yuri.uart_write import UartWrite
from yuri.stream import Stream
from yuri.timer import Timer
import time

def sendLiveSingle():
    stream = Stream()
    stream.write_short(1226)
    stream.write_byte(0)
    UartWrite.get_instance().write(stream.get_bytes())
    
tt = Timer(sendLiveSingle, 1000*1)
while True:
    time.sleep(200/1000)
    tt.tick()