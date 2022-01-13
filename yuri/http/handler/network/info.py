# my_api.py
import sys, machine
import network, time
from yuri.stream import Stream
import gc

class Handler:
    def __init__(self):
        pass
    
    def get(self, api_request):
        #print(api_request['http']['debug'])

        info = {}
        with open('/tmp/interface.bin', 'rb') as f:
            stream = Stream(f.read())
            info['ap'] = {}
            if stream.readByte() == 1:
                info['ap']['ssid'] = stream.readStr()
                info['ap']['password'] = stream.readStr()
                info['ap']['address'] = stream.readStr()
                info['ap']['mac'] = stream.readStr()

            info['wifi'] = {}
            if stream.readByte() == 1:
                info['wifi']['ssid'] = stream.readStr()
                info['wifi']['password'] = stream.readStr()
                info['wifi']['address'] = stream.readStr()
                info['wifi']['mac'] = stream.readStr()
        gc.collect()
        return info
