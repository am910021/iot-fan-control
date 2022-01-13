import gc, sys, time, os
from yuri.NetworkHelper import NetworkHelper

network = NetworkHelper()
network.do_connect()
network.create_ap()
network.save_info()
NetworkHelper.release() #release used memory.
print(gc.mem_free())
del globals()['NetworkHelper']
del sys.modules['yuri.NetworkHelper']
if 'network' in globals():
    del globals()['network']
if 'yuri' in globals():
    del globals()['yuri']
time.sleep(1)
gc.collect()
time.sleep(1)
print(gc.mem_free())
from yuri.logger import logger
from yuri.http.tcpserver import TCPServer
from yuri.http.config import default as default_config
from yuri.http.processor.api import ApiProcess
from yuri.http.processor.file import FileProcess
from yuri.http.handler import my_api, my_api2, api3, network_info, fan_control
from yuri.http.processor import Processor
print(gc.mem_free())

config = default_config()
config['port'] = 80
api_handler = ApiProcess([
        (['test'], my_api.Handler()),
        (['test2'], my_api2.Handler()),
        (['test3'], api3.Handler()),
        (['info'], info.Handler()),
        (['fan'], fan_control.Handler())
    ])

processor = Processor(handlers=[
        ('/api', api_handler),
        ('/', FileProcess('/www'))
    ], config=config)
server = TCPServer(processor, config={'address': '0.0.0.0',
                                          'port': 80,
                                          'timeout': 30, })
server.start()
print(gc.mem_free())