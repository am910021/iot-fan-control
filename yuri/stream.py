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

    def _canWrite(self, size=0):
        if self.length() + size > self._limit:
            raise StreamException(
                "Stream out of range, available write size is {}.".format(self._limit - self.length()))

    def write(self, w: bytes):
        self._canWrite(len(w))
        self._data += w

    def read(self, size: int) -> bytes:
        if self.length() < size:
            raise StreamException("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:size]
        self._data = self._data[size:]
        return r

    def writeByte(self, w: int):
        self._canWrite(1)
        if w < BYTE_MIN or w > BYTE_MAX:
            raise ByteOutOfRange("Out of range,the range  is {} ~ {}".format(BYTE_MIN, BYTE_MAX))
        self._data += struct.pack('b', w)

    def readByte(self) -> int:
        if self.length() == 0:
            raise ByteOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:1]
        self._data = self._data[1:]
        return struct.unpack('<b', r)[0]

    def writeShort(self, w: int):
        self._canWrite(2)
        if w < SHORT_MIN or w > SHORT_MAX:
            raise ShortOutOfRange("Out of range,the range  is {} ~ {}".format(SHORT_MIN, SHORT_MAX))
        self._data += struct.pack('h', w)

    def readShort(self) -> int:
        if self.length() < 2:
            raise ShortOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:2]
        self._data = self._data[2:]
        return struct.unpack('<h', r)[0]

    def writeInt(self, w: int):
        self._canWrite(4)
        if w < INTEGER_MIN or w > INTEGER_MAX:
            raise IntegerOutOfRange("Out of range,the range is {} ~ {}".format(INTEGER_MIN, INTEGER_MAX))
        self._data += struct.pack('i', w)

    def readInt(self) -> int:
        if self.length() < 4:
            raise IntegerOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:4]
        self._data = self._data[4:]
        return struct.unpack('<i', r)[0]

    def writeLong(self, w: int):
        self._canWrite(8)
        if w < LONG_MIN or w > LONG_MAX:
            raise LongOutOfRange("Out of range,the range  is {} ~ {}".format(LONG_MIN, LONG_MAX))
        self._data += struct.pack('q', w)

    def readLong(self) -> int:
        if self.length() < 8:
            raise LongOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:8]
        self._data = self._data[8:]
        return struct.unpack('<q', r)[0]

    def writeFloat(self, w: float):
        self._canWrite(8)
        if w < FLOAT_MIN or w > FLOAT_MAX:
            raise FloatOutOfRange("Out of range,the range is {} ~ {}".format(FLOAT_MIN, FLOAT_MAX))
        self._data += struct.pack('d', w)

    def readFloat(self) -> float:
        if self.length() < 8:
            raise FloatOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        r = self._data[0:8]
        self._data = self._data[8:]
        return struct.unpack('<d', r)[0]

    def writeStr(self, wo: str):
        w = wo.encode('UTF-8')
        size = len(w)
        self._canWrite(size)
        if size > SHORT_MAX:
            raise StringOutOfRange(
                "Out of the range, the maximum byte length of the utf8 string is {}.".format(SHORT_MAX))

        self._data += struct.pack('h', size)
        self._data += w

    def readStr(self) -> str:
        size = self.readShort()
        if self.length() < size:
            raise StringOutOfRange("Stream out of range, available size is {}.".format(self.length()))

        string = self._data[0:size]
        self._data = self._data[size:]
        return string.decode('UTF-8')

    def getBytes(self) -> bytes:
        return self._data

    def printHex(self):
        print(' '.join('{:02X}'.format(a) for a in self._data))


if __name__ == '__main__':
    print("This is module file, not executable file.")
    # print(ustruct == struct)

    # stream = Stream()

    # stream.writeStr("我")
    # stream.writeInt(-2147483648)
    # print(stream.getBytes())
    # print(stream._data)
    # stream.printHex()
    # print(stream.readStr())
    # print(stream.readInt())

    # stream.writeStr("我我我")
    # print(stream.readStr())

    # stream.writeByte(-128)
    # stream.writeByte(127)

    # stream.writeShort(-32768)
    # stream.writeShort(32767)

    # stream.writeInt(-2147483648)
    # stream.writeInt(2147483647)

    # stream.writeLong(-9223372036854775808)
    # stream.writeLong(9223372036854775807)

    # stream.printHex()
    # print(stream._data)

    # print(stream.readByte())
    # print(stream.readByte())
    # print(stream.readShort())
    # print(stream.readShort())
    # print(stream.readInt())
    # print(stream.readInt())
    # print(stream.readLong())
    # print(stream.readLong())
