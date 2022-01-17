import gc, sys, time, os
from yuri.logger import logger
from yuri.network_daemon import NetworkHelper

#設定logger 等級0=debug 1=info 2=warring 3=error
logger.set_levels([1])

#enable network ap / wifi.
network = NetworkHelper()
network.do_connect()
network.create_ap()
network.save_info()
NetworkHelper.release() #release used memory.

del globals()['NetworkHelper']
del sys.modules['yuri.network_daemon']
if 'network' in globals():
    del globals()['network']
if 'yuri' in globals():
    del globals()['yuri']
if 'logger' in globals():
    del globals()['logger']
if 'network' in sys.modules:
    del sys.modules['network']

gc.collect()
