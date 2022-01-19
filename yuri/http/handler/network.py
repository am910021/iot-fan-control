# my_api.py
import sys
from yuri.http.response import Html
from yuri.http.share import dict_update
import gc


class Info:
    def __init__(self):
        pass

    def get(self, api_request):
        gc.collect()
        info = {}
        info['page_title'] = 'Network daemon'
        null = "null"
        Stream = getattr(getattr(__import__('yuri.stream_lite'), 'stream_lite'), 'Stream')
        with open('/tmp/interface.bin', 'rb') as f:
            stream = Stream(f.read())
            if stream.read_byte() == 1:
                info['ap_enable'] = True
                info['ap_ssid'] = stream.read_str()
                info['ap_passwd'] = stream.read_str()
                info['ap_ip'] = stream.read_str()
                info['ap_mac'] = stream.read_str()
            else:
                info['ap_enable'] = False
                info['ap_ssid'] = stream.read_str()
                info['ap_passwd'] = stream.read_str()
                info['ap_mac'] = stream.read_str()
                info['ap_ip'] = null

            if stream.read_byte() == 1:
                info['wifi_enable'] = True
                info['wifi_ssid'] = stream.read_str()
                info['wifi_passwd'] = stream.read_str()
                info['wifi_ip'] = stream.read_str()
                info['wifi_mac'] = stream.read_str()
            else:
                info['wifi_enable'] = False
                info['wifi_ssid'] = stream.read_str()
                info['wifi_passwd'] = stream.read_str()
                info['wifi_mac'] = stream.read_str()
                info['wifi_ip'] = null
            f.close()
            del sys.modules['yuri.stream_lite']
            gc.collect()
        return Html.response('network/info.html', info)


class Edit:
    def __init__(self):
        pass

    def post(self, request):
        gc.collect()
        config = getattr(getattr(__import__('yuri.sys_config'), 'sys_config'), 'config')
        http, ap, wifi = config.http, config.ap, config.wifi
        config = None
        del sys.modules['yuri.sys_config']
        gc.collect()

        ap['enable'] = True if 'ae' in request['body'] else False
        if request['body']['as'] != '':
            ap['ssid'] = request['body']['as']
        else:
            return Edit.error_response('AP SSID is empty')

        if request['body']['ap'] != '':
            ap['password'] = request['body']['ap']
        else:
            return Edit.error_response('AP PWD is empty')

        wifi['enable'] = True if 'we' in request['body'] else False
        if request['body']['ws'] != '':
            wifi['ssid'] = request['body']['ws']
        else:
            return Edit.error_response('WIFI SSID is empty')

        if request['body']['wp'] != '':
            wifi['password'] = request['body']['wp']
        else:
            return Edit.error_response('WIFI PWD')

        json = __import__('json')
        setting = {'http':http, 'ap':ap, 'wifi':wifi}
        with open('config.txt', 'w') as jsonfile:
            json.dump(setting, jsonfile)
        json = None
        return Html.response('network/edit.html', dict_update(Edit.get_info(), {
            'success': 'config save success, please click reboot button.'}))

    def get(self, api_request):
        gc.collect()
        return Html.response('network/edit.html', Edit.get_info())

    @staticmethod
    def error_response(msg: str):
        return Html.response('network/edit.html', dict_update(Edit.get_info(), {'error': msg}))

    @staticmethod
    def get_info():
        info = {}
        info['page_title'] = 'Network edit'
        config = getattr(getattr(__import__('yuri.sys_config'), 'sys_config'), 'config')
        ap, wifi = dict(config.ap), dict(config.wifi)
        config = None
        del sys.modules['yuri.sys_config']
        gc.collect()
        info['ae'] = 'checked' if ap['enable'] else ''
        info['as'] = ap['ssid']
        info['ap'] = ap['password']
        info['we'] = 'checked' if wifi['enable'] else ''
        info['ws'] = wifi['ssid']
        info['wp'] = wifi['password']
        return info


class Reboot:
    def __init__(self):
        pass

    def get(self, request):
        params = {'page_title': 'Reboot info'}
        return Html.response('reboot/info.html', data=params)

    def post(self, request):
        params = {'page_title': 'Rebooting'}
        return Html.response('reboot/success.html', data=params, callback=self.reboot)

    def reboot(self):
        machine = __import__('machine')
        machine.reset()