# my_api.py
import sys, machine, gc
from yuri.http.response import Html
from yuri.stream_lite import Stream


class RTable:
    def __init__(self):
        pass

    def get(self, request):
        info = {'title': 'R Table info'}
        R = [
            [-1, -1, -1, -1, 0, -1],
            [-1, -1, -1, 0, -1, 100],
            [-1, -1, -1, 0, -1, -1],
            [-1, 0, 0, -1, 0, -1],
            [0, -1, -1, 0, -1, 100],
            [-1, 0, -1, -1, 0, 100]
        ]

        b = '    ' + '  '.join(['{0: >3}'.format(e + 1) for e in range(len(R))]) + '\n'
        b += '   |' + '-'.join(['----' for e in range(len(R))]) + '\n'
        for i in range(len(R)):
            b += '{0: >4}'.format(str(i + 1) + '|')
            b += ', '.join(['{0: >3}'.format(e) for e in R[i]]) + '\n'

        info['rt'] = b
        return Html.response('fan/r/info.html', info)

    def post(self, request):
        pass


def tw():
    R = [
        [-1, -1, -1, -1, 0, -1],
        [-1, -1, -1, 0, -1, 100],
        [-1, -1, -1, 0, -1, -1],
        [-1, 0, 0, -1, 0, -1],
        [0, -1, -1, 0, -1, 100],
        [-1, 0, -1, -1, 0, 100]
    ]
    stream = Stream()
    stream.write_byte(len(R))
    for i in R:
        for j in i:
            stream.write_byte(j)

    with open('r.table', 'wb') as f:
        f.write(stream.get_bytes())


def tr():
    # Stream = getattr(getattr(__import__('yuri.stream_lite'), 'stream_lite'), 'Stream')
    R = None
    with open('r.table', 'rb') as f:
        stream = Stream(f.read())
        size = stream.read_byte()
        R = [[0] * size] * size
        for i in range(size):
            for j in range(size):
                R[i][j] = stream.read_byte()
    print(R)