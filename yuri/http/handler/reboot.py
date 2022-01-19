from yuri.http.response import Html


class Handler:
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
