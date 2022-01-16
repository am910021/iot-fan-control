from yuri.http.response import Json
from yuri.stream import Stream
import gc

class Handler:
    def __init__(self):
        pass
    
    def get(self, api_request):
        info = {}
        with open('/tmp/interface.bin', 'rb') as f:
            stream = Stream(f.read())
            info['ap'] = {}
            if stream.read_bool():
                info['ap']['ssid'] = stream.read_str()
                info['ap']['password'] = stream.read_str()
                info['ap']['address'] = stream.read_str()
                info['ap']['mac'] = stream.read_str()
            else:
                stream.read_str()
                stream.read_str()

            info['wifi'] = {}
            if stream.read_bool():
                info['wifi']['ssid'] = stream.read_str()
                info['wifi']['password'] = stream.read_str()
                info['wifi']['address'] = stream.read_str()
                info['wifi']['mac'] = stream.read_str()
            else:
                stream.read_str()
                stream.read_str()
        gc.collect()
        return Json.response(info)
