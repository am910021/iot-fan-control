from yuri.uart_write import UartWrite
from yuri.stream import Stream
from yuri.timer import Timer
import time

def sendLiveSingle():
    stream = Stream()
    stream.writeShort(1226)
    stream.writeByte(0)
    UartWrite.get_instance().write(stream.getBytes())
    
tt = Timer(sendLiveSingle, 1000*1)
while True:
    time.sleep(200/1000)
    tt.tick()