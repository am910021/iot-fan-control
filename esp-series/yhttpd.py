import gc, sys
# from yuri.stream import Stream
from yuri.sys_config import config as sys_config
from yuri.http.tcpserver import TCPServer
# from yuri.http.processor.api import ApiProcess
from yuri.http.processor.file import FileProcess
from yuri.http.processor.logic import LogicProcess
# from yuri.http.handler import my_api, my_api2, api3, fan_control, network_edit, network_info
from yuri.http.handler import network_info2
from yuri.http.handler import network_edit2
from yuri.http.processor import Processor
from yuri.logger import logger

logger.set_levels([0, 1, 2, 3])

config = dict(sys_config.http)
del globals()['sys_config']
del sys.modules['yuri.sys_config']

# api_handler = ApiProcess([
#     (['test'], my_api.Handler()),
#     (['test2'], my_api2.Handler()),
#     (['test3'], api3.Handler()),
#     (['network', 'info'], network_info.Handler()),
#     (['network', 'edit'], network_edit.Handler()),
#     (['fan'], fan_control.Handler())
# ])

api2_handler = LogicProcess([
    (['info'], network_info2.Handler()),
    (['edit'], network_edit2.Handler()),
])

processor = Processor(handlers=[
    ('/network', api2_handler),
    # ('/api', api_handler),
    ('/', FileProcess('/www'))
], config=config)
server = TCPServer(processor, config=config)
server.start()
gc.collect()
