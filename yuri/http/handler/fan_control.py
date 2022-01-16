# my_api.py
import sys, machine, gc
from yuri.stream import Stream
from yuri.uart_write import uart

class Handler:
    def __init__(self):
        pass
    
    def get(self, api_request):
        params = api_request['query_params']
        #if not api_request['http']['debug']:
        #    return {'msg': 'debug mode can\'t control fan.'}
        
        if not params or not 'ctrl' in params:
            return {'msg': 'params error.'}
        
        ctrls=params['ctrl'].split(',')
        if len(ctrls) != 6:
            return {'msg': 'size is %d not 6.' % (len(ctrls))}
        
        stream = Stream()
        for ctrl in ctrls:
            stream.write_byte(int(ctrl))
        uart.write(stream.get_bytes())
        gc.collect()
        return {'name': 'api-3'}