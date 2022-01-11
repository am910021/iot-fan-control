import gc, sys
from yuri.stream import Stream
from yuri.config import config as gConfig
from yuri.http.tcpserver import TCPServer
from yuri.http.processor.api import ApiProcess
from yuri.http.processor.file import FileProcess
from yuri.http.handler import my_api, my_api2, api3, info, fan_control
from yuri.http.processor import Processor
from yuri.logger import logger


logger.setLevels([0, 1, 2, 3])

config = dict(gConfig.http)
del globals()['gConfig']
del sys.modules['yuri.config']

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
server = TCPServer(processor, config=config)
server.start()
gc.collect()