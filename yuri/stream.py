import struct


class StreamException(Exception):
    pass


class ByteOutOfRange(Exception):
    pass


class ShortOutOfRange(Exception):
    pass


class IntegerOutOfRange(Exception):
    pass


class LongOutOfRange(Exception):
    pass


class FloatOutOfRange(Exception):
    pass


class StringOutOfRange(Exception):
    pass


BYTE_MAX = 127
BYTE_MIN = -128
SHORT_MAX = 0x7fff
SHORT_MIN = -0x7fff - 1
INTEGER_MAX = 0x7fffffff
INTEGER_MIN = -0x7fffffff - 1
LONG_MAX = 0x7fffffffffffffff
LONG_MIN = -0x7fffffffffffffff - 1
FLOAT_MAX = 3.4028235E38
FLOAT_MIN = 1.4E-45
DOUBLE_MAX = 1.7976931348623157E308
DOUBLE_MIN = 4.9E-324


class Stream:
    def __init__(self, stream="".encode(), limit=INTEGER_MAX):
        self._data = stream
        self._limit = limit

    def length(self):
        return len(self._data)

    def _can_write(self, size=0):
        if self.length() + size > self._limit:
            raise StreamException(
                "Stream out of range, available write size is {}.".format(self._limit - self.length()))

    def write(self, w: bytes):
        self._can_write(len(w))
        self._data += w

    def read(self, size: int) -> bytes:
        if self.length() < size:
            raise StreamException("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:size]
        self._data = self._data[size:]
        return r

    def write_byte(self, w: int):
        self._can_write(1)
        if w < BYTE_MIN or w > BYTE_MAX:
            raise ByteOutOfRange("Out of range,the range  is {} ~ {}".format(BYTE_MIN, BYTE_MAX))
        self._data += struct.pack('b', w)

    def read_byte(self) -> int:
        if self.length() == 0:
            raise ByteOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:1]
        self._data = self._data[1:]
        return struct.unpack('<b', r)[0]

    def write_bool(self, i: bool):
        self._can_write(1)
        w = 1 if i else 0
        if w < BYTE_MIN or w > BYTE_MAX:
            raise ByteOutOfRange("Out of range,the range  is {} ~ {}".format(BYTE_MIN, BYTE_MAX))
        self._data += struct.pack('b', w)

    def read_bool(self) -> bool:
        if self.length() == 0:
            raise ByteOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        i = self._data[0:1]
        self._data = self._data[1:]
        r = struct.unpack('<b', i)[0] == 1
        return r

    def write_short(self, w: int):
        self._can_write(2)
        if w < SHORT_MIN or w > SHORT_MAX:
            raise ShortOutOfRange("Out of range,the range  is {} ~ {}".format(SHORT_MIN, SHORT_MAX))
        self._data += struct.pack('h', w)

    def read_short(self) -> int:
        if self.length() < 2:
            raise ShortOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:2]
        self._data = self._data[2:]
        return struct.unpack('<h', r)[0]

    def write_int(self, w: int):
        self._can_write(4)
        if w < INTEGER_MIN or w > INTEGER_MAX:
            raise IntegerOutOfRange("Out of range,the range is {} ~ {}".format(INTEGER_MIN, INTEGER_MAX))
        self._data += struct.pack('i', w)

    def read_int(self) -> int:
        if self.length() < 4:
            raise IntegerOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:4]
        self._data = self._data[4:]
        return struct.unpack('<i', r)[0]

    def write_long(self, w: int):
        self._can_write(8)
        if w < LONG_MIN or w > LONG_MAX:
            raise LongOutOfRange("Out of range,the range  is {} ~ {}".format(LONG_MIN, LONG_MAX))
        self._data += struct.pack('q', w)

    def read_long(self) -> int:
        if self.length() < 8:
            raise LongOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:8]
        self._data = self._data[8:]
        return struct.unpack('<q', r)[0]

    def write_float(self, w: float):
        self._can_write(8)
        if w < FLOAT_MIN or w > FLOAT_MAX:
            raise FloatOutOfRange("Out of range,the range is {} ~ {}".format(FLOAT_MIN, FLOAT_MAX))
        self._data += struct.pack('d', w)

    def read_float(self) -> float:
        if self.length() < 8:
            raise FloatOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:8]
        self._data = self._data[8:]
        return struct.unpack('<d', r)[0]

    def write_str(self, wo: str):
        w = wo.encode('UTF-8')
        size = len(w)
        self._can_write(size)
        if size > SHORT_MAX:
            raise StringOutOfRange(
                "Out of the range, the maximum byte length of the utf8 string is {}.".format(SHORT_MAX))

        self._data += struct.pack('h', size)
        self._data += w

    def read_str(self) -> str:
        size = self.read_short()
        if self.length() < size:
            raise StringOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        string = self._data[0:size]
        self._data = self._data[size:]
        return string.decode('UTF-8')

    def get_bytes(self) -> bytes:
        return self._data

    def print_hex(self):
        print(' '.join('{:02X}'.format(a) for a in self._data))


if __name__ == '__main__':
    print("This is module file, not executable file.")
    # print(ustruct == struct)

    # stream = Stream()

    # stream.write_str("我")
    # stream.write_int(-2147483648)
    # print(stream.get_bytes())
    # print(stream._data)
    # stream.print_hex()
    # print(stream.read_str())
    # print(stream.read_int())

    # stream.write_str("我我我")
    # print(stream.read_str())

    # stream.write_byte(-128)
    # stream.write_byte(127)

    # stream.write_short(-32768)
    # stream.write_short(32767)

    # stream.write_int(-2147483648)
    # stream.write_int(2147483647)

    # stream.write_long(-9223372036854775808)
    # stream.write_long(9223372036854775807)

    # stream.print_hex()
    # print(stream._data)

    # print(stream.read_byte())
    # print(stream.read_byte())
    # print(stream.read_short())
    # print(stream.read_short())
    # print(stream.read_int())
    # print(stream.read_int())
    # print(stream.read_long())
    # print(stream.read_long())
