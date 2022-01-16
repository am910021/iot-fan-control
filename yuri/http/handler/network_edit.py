# my_api.py
import sys, machine
import network, time
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
        return b'<h1>Hello</h1>'