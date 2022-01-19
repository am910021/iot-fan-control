# my_api.py
from yuri.http.response import File


class Index:
    def get(self, request):
        return File.response('/www/index.html', 'text/html')


class Ico:
    def get(self, request):
        return File.response('/www/favicon.ico', 'image/x-icon')
