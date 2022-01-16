import struct, time
from yuri.stream import Stream

BYTE_MAX =    int(0xff / 2)
BYTE_MIN =    (int(0xff / 2)+1)*-1

SHORT_MAX =   int(0xffff / 2)
SHORT_MIN =   (int(0xffff / 2)+1)*-1

INTEGER_MAX = int(0xffffffff / 2)-1
INTEGER_MIN = int(0xffffffff / 2)*-1

LONG_MAX =    int(0xffffffffffffffff / 2)-1
LONG_MIN =    int(0xffffffffffffffff / 2)*-1

if __name__ == '__main__':
    t1 = struct.pack('B', 1)
    t2 = struct.pack('b', 2)
    t3 = struct.pack('b', 3)
    t4 = t1+t2+t3
    print(t4)
    
    data1 = -127
    data2 = 128
    
    data_h = 0xff / 2
    print(int(data_h*-1)-1)
    print(int(data_h))
    
    print(BYTE_MIN, BYTE_MAX)
    print(SHORT_MIN, SHORT_MAX)
    print(INTEGER_MIN, INTEGER_MAX)
    print(LONG_MIN, LONG_MAX)
    
    print(-1.7976931348623157e+308)
    
    start=time.ticks_ms()
    stream = Stream()
    
    stream.write_str("我")
    stream.write_int(-2147483648)
    print(stream.get_bytes())
    print(stream._data)
    stream.print_hex()
    print(stream.read_str())
    print(stream.read_int())
    end=time.ticks_ms()
    print(end-start, "ms")
    