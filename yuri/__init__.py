import gc, sys, time, os
from yuri.NetworkHelper import NetworkHelper

print(gc.mem_free())

#enable network ap / wifi.
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

