# my_api.py
import sys

from yuri.http.response import Html
from ..share import dict_update
import gc


class Handler:
    def __init__(self):
        pass

    def post(self, request):
        gc.collect()
        params = request['body']
        config = getattr(getattr(__import__('yuri.sys_config'), 'sys_config'), 'config')

        config.ap['enable'] = True if 'ap_enable' in params else False
        if params['ap_ssid'] != '':
            config.ap['ssid'] = params['ap_ssid']
        else:
            return Handler.error_response('AP SSID is empty')

        if params['ap_passwd'] != '':
            config.ap['password'] = params['ap_passwd']
        else:
            return Handler.error_response('AP PWD is empty')

        config.wifi['enable'] = True if 'wifi_enable' in params else False
        if params['wifi_ssid'] != '':
            config.wifi['ssid'] = params['wifi_ssid']
        else:
            return Handler.error_response('WIFI SSID is empty')

        if params['wifi_passwd'] != '':
            config.wifi['password'] = params['wifi_passwd']
        else:
            return Handler.error_response('WIFI PWD')

        config.save_config()
        del sys.modules['yuri.sys_config']
        return Html.response('network/edit.html', dict_update(Handler.get_info(), {
            'success': 'config save success, please click reboot button.'}))

    def get(self, api_request):
        gc.collect()
        return Html.response('network/edit.html', Handler.get_info())

    @staticmethod
    def error_response(msg: str):
        return Html.response('network/edit.html', dict_update(Handler.get_info(), {'error': msg}))

    @staticmethod
    def get_info():
        info = {}
        info['page_title'] = 'Network edit'
        config = getattr(getattr(__import__('yuri.sys_config'), 'sys_config'), 'config')
        info['ap_enable'] = 'checked' if config.ap['enable'] else ''
        info['ap_ssid'] = config.ap['ssid']
        info['ap_passwd'] = config.ap['password']
        info['wifi_enable'] = 'checked' if config.wifi['enable'] else ''
        info['wifi_ssid'] = config.wifi['ssid']
        info['wifi_passwd'] = config.wifi['password']
        del sys.modules['yuri.sys_config']
        return info
