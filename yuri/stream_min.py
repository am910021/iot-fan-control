import struct


class Stream:
    def __init__(self, stream=b"", limit=None):
        self._data = stream

    def length(self):
        return len(self._data)

    def _get_buff(self, size):
        buff = self._data[0:size]
        self._data = self._data[size:]
        return buff

    def write(self, w: bytes):
        self._data += w

    def read(self, size: int) -> bytes:
        return self._get_buff(size)

    def write_byte(self, w: int):
        self._data += struct.pack('b', w)

    def read_byte(self) -> int:
        return struct.unpack('<b', self._get_buff(1))[0]

    def write_bool(self, w: bool):
        self.write_byte(1 if w else 0)

    def read_bool(self) -> bool:
        return self.read_byte() == 1

    def write_short(self, w: int):
        self._data += struct.pack('h', w)

    def read_short(self) -> int:
        return struct.unpack('<h', self._get_buff(2))[0]

    def write_int(self, w: int):
        self._data += struct.pack('i', w)

    def read_int(self) -> int:
        return struct.unpack('<i', self._get_buff(4))[0]

    def write_long(self, w: int):
        self._data += struct.pack('q', w)

    def read_long(self) -> int:
        return struct.unpack('<q', self._get_buff(8))[0]

    def write_float(self, w: float):
        self._data += struct.pack('d', w)

    def read_float(self) -> float:
        return struct.unpack('<d', self._get_buff(8))[0]

    def write_str(self, wo: str):
        w = wo.encode('UTF-8')
        size = len(w)
        self._data += struct.pack('h', size)
        self._data += w

    def read_str(self) -> str:
        size = self.read_short()
        return self._get_buff(size).decode('UTF-8')

    def get_bytes(self, nocheck=False) -> bytes:
        if nocheck:
            return self._data
        return struct.pack('i', self.length()) + self._data

    def print_hex(self):
        print(' '.join('{:02X}'.format(a) for a in self._data))


