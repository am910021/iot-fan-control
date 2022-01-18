# my_api.py
import sys,json
from yuri.http.response import Html
from yuri.http.share import dict_update
import gc


class Handler:
    def __init__(self):
        pass

    def post(self, request):
        gc.collect()
        params = request['body']
        config = getattr(getattr(__import__('yuri.sys_config'), 'sys_config'), 'config')
        config.ap['enable'] = True if 'ae' in params else False
        if params['as'] != '':
            config.ap['ssid'] = params['as']
        else:
            return Handler.error_response('AP SSID is empty')

        if params['ap'] != '':
            config.ap['password'] = params['ap']
        else:
            return Handler.error_response('AP PWD is empty')

        config.wifi['enable'] = True if 'we' in params else False
        if params['ws'] != '':
            config.wifi['ssid'] = params['ws']
        else:
            return Handler.error_response('WIFI SSID is empty')

        if params['wp'] != '':
            config.wifi['password'] = params['wp']
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
