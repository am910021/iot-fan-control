import struct

BYTE_MAX = 127
BYTE_MIN = -128
INTEGER_MAX = 0x7fffffff
INTEGER_MIN = -0x7fffffff - 1
FLOAT_MAX = 3.4028235E38
FLOAT_MIN = 1.4E-45
STRING_MAX = 512


class Stream:
    def __init__(self, stream=b"", limit=2048):
        self._data = stream
        self._limit = limit

    def length(self):
        return len(self._data)

    def _get_buff(self, size):
        buff = self._data[0:size]
        self._data = self._data[size:]
        return buff

    def _check_write_length(self, size=0):
        if self.length() + size > self._limit:
            raise Exception("Stream out of range, available write size is {}.".format(self._limit - self.length()))

    def _check_write(self, size, w, minimum, maximum, err):
        self._check_write_length(size)
        if (w < minimum) or (w > maximum):
            raise Exception("{} out of range,the range  is {} ~ {}".format(err, min, max))

    def _check_read(self, size, err):
        if self.length() < size:
            raise Exception("{} stream out of range, available size is {}.".format(err, self.length()))

    def write(self, w: bytes):
        self._check_write_length(len(w))
        self._data += w

    def read(self, size: int) -> bytes:
        self._check_read(size, 'Buff')
        return self._get_buff(size)

    def write_byte(self, w: int):
        self._check_write(1, w, BYTE_MIN, BYTE_MAX, 'Byte')
        self._data += struct.pack('b', w)

    def read_byte(self) -> int:
        self._check_read(1, 'Byte')
        return struct.unpack('<b', self._get_buff(1))[0]

    def write_int(self, w: int):
        self._check_write(4, w, INTEGER_MIN, INTEGER_MAX, 'Integer')
        self._data += struct.pack('i', w)

    def read_int(self) -> int:
        self._check_read(4, 'Integer')
        return struct.unpack('<i', self._get_buff(4))[0]

    def write_float(self, w: float):
        self._check_write(8, w, FLOAT_MIN, FLOAT_MAX, 'Float')
        self._data += struct.pack('d', w)

    def read_float(self) -> float:
        self._check_read(8, 'Float')
        return struct.unpack('<d', self._get_buff(8))[0]

    def write_str(self, wo: str):
        w = wo.encode('UTF-8')
        size = len(w)
        self._check_write_length(size + 1)
        if size > STRING_MAX:
            raise Exception(
                "String out of the range, the maximum byte length of the utf8 string is {}.".format(STRING_MAX))
        self._data += struct.pack('h', size)
        self._data += w

    def read_str(self) -> str:
        size = struct.unpack('<h', self._get_buff(2))[0]
        self._check_read(size, 'String')
        return self._get_buff(size).decode('UTF-8')

    def get_bytes(self, nocheck=False) -> bytes:
        if nocheck:
            return self._data
        return struct.pack('i', self.length()) + self._data

    def print_hex(self):
        print(' '.join('{:02X}'.format(a) for a in self._data))


# if __name__ == '__main__':
#     ostream = Stream()
#     ostream.write_byte(0)
#     ostream.write_int(999999999)
#     ostream.write_float(0.5)
#     ostream.write_str('testtest')
#     ostream.print_hex()
#
#     buff = ostream.get_bytes()
#
#     istream = Stream(buff)
#     istream.print_hex()
#     print(istream.read_int() == istream.length())