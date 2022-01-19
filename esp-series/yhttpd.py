import gc, sys
from yuri.sys_config import config as sys_config
from yuri.http.tcpserver import TCPServer
from yuri.http.processor.file import FileProcess
from yuri.http.processor.logic import LogicProcess
from yuri.http.handler import network
from yuri.http.processor import Processor
from yuri.logger import logger

logger.set_levels([0, 1, 2, 3])

config = dict(sys_config.http)
del globals()['sys_config']
del sys.modules['yuri.sys_config']

network_handler = LogicProcess([
    (['info'], network.Info()),
    (['edit'], network.Edit()),
    (['reboot'], network.Reboot()),
])

processor = Processor(handlers=[
    ('/network', network_handler),
    ('/', FileProcess('/www'))
], config=config)
server = TCPServer(processor, config=config)
server.start()
gc.collect()
