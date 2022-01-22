import gc, sys, time, os
from yuri.logger import logger
from yuri.network_daemon import NetworkHelper

# 設定logger 等級0=debug 1=info 2=warring 3=error
logger.set_levels([0, 1, 2, 3])

# enable network ap / wifi.
network = NetworkHelper()
network.do_connect()
network.create_ap()
network.save_info()
NetworkHelper.release()  # release used memory.

del globals()['network']
del globals()['NetworkHelper']
del sys.modules['yuri.network_daemon']
del globals()['logger']
del sys.modules['yuri.logger']

gc.collect()
