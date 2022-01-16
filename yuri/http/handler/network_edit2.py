# my_api.py
import sys, machine
import network, time

from yuri.http.response import Html
from yuri.stream import Stream
import gc


class Handler:
    def __init__(self):
        pass

    def post(self, api_request):
        print(api_request)
        gc.collect()
        return {"test":"pass"}

    def get(self, api_request):
        gc.collect()
        info = {}
        info['page_title'] = 'Network edit'
        null = "null"
        with open('/tmp/interface.bin', 'rb') as f:
            stream = Stream(f.read())
            if stream.read_bool():
                info['ap_enable'] = 'true'
                info['ap_c'] = 'checked'
                info['ap_ssid'] = stream.read_str()
                info['ap_passwd'] = stream.read_str()
                stream.read_str()
                stream.read_str()
            else:
                info['ap_enable'] = 'false'
                info['ap_c'] = ''
                info['ap_ssid'] = stream.read_str()
                info['ap_passwd'] = stream.read_str()

            if stream.read_bool():
                info['wifi_enable'] = 'true'
                info['wifi_c'] = 'checked'
                info['wifi_ssid'] = stream.read_str()
                info['wifi_passwd'] = stream.read_str()
                stream.read_str()
                stream.read_str()
            else:
                info['wifi_enable'] = 'false'
                info['wifi_c'] = ''
                info['wifi_ssid'] = stream.read_str()
                info['wifi_passwd'] = stream.read_str()

        return Html.response('network/edit.html', info)