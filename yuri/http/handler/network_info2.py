# my_api.py
from yuri.http.response import Html
from yuri.stream import Stream
import gc
from yuri.logger import logger


class Handler:
    def __init__(self):
        pass

    def get(self, api_request):
        gc.collect()
        info = {}
        info['page_title'] = 'Network daemon'
        null = "null"
        with open('/tmp/interface.bin', 'rb') as f:
            stream = Stream(f.read())
            if stream.read_bool():
                info['ap_enable'] = True
                info['ap_ssid'] = stream.read_str()
                info['ap_passwd'] = stream.read_str()
                info['ap_ip'] = stream.read_str()
                info['ap_mac'] = stream.read_str()
            else:
                info['ap_enable'] = False
                info['ap_ssid'] = stream.read_str()
                info['ap_passwd'] = stream.read_str()
                info['ap_ip'] = null
                info['ap_mac'] = null

            if stream.read_bool():
                info['wifi_enable'] = True
                info['wifi_ssid'] = stream.read_str()
                info['wifi_passwd'] = stream.read_str()
                info['wifi_ip'] = stream.read_str()
                info['wifi_mac'] = stream.read_str()
            else:
                info['wifi_enable'] = False
                info['wifi_ssid'] = stream.read_str()
                info['wifi_passwd'] = stream.read_str()
                info['wifi_ip'] = null
                info['wifi_mac'] = null
        return Html.response('network/info.html', info)
