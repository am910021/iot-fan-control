import gc, sys
from yuri.sys_config import config as sys_config
from yuri.http.tcpserver import TCPServer
# from yuri.http.processor.file import FileProcess
from yuri.http.processor.logic import LogicProcess
from yuri.http.handler import network, Index, Ico

from yuri.http.handler import fan_control
from yuri.http.processor import Processor
from yuri.logger import logger

logger.set_levels([3])

config = dict(sys_config.http)
del globals()['sys_config']
del sys.modules['yuri.sys_config']

network_handler = LogicProcess([
    ([''], Index()),
    (['index.html'], Index()),
    (['favicon.ico', Ico()]),
    (['network', 'info'], network.Info()),
    (['network', 'edit'], network.Edit()),
    (['network', 'reboot'], network.Reboot()),
    (['table', 'info'], fan_control.RTable()),
])

# fan_handler = LogicProcess([
#    (['r', 'info'], fan_control.RTable()),
# ])

processor = Processor(handlers=[
    ('/', network_handler),
    #    ('/fan', fan_handler),
    #    ('/', FileProcess('/www'))
], config=config)
server = TCPServer(processor, config=config)
server.start()
gc.collect()
