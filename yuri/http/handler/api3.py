# my_api.py
import sys, machine
from machine import UART, Pin

class Handler:
    def __init__(self):
        pass
    
    def get(self, api_request):
        #print('dev', api_request['http']['dev'])
        
        params = api_request['query_params']
        
        if params and 'exit' in params:
            #machine.soft_reset()
            sys.exit(1)
        if params and 'reset' in params:
            machine.reset()
        gc.collect()
        return {'name': 'api-3'}