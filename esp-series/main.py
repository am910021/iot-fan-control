import gc, sys

# python為直譯程式，import即可執行networkd
import networkd

# 移除除執行過的網路連線程式networkd
del globals()['networkd']
del globals()['bdev']
del globals()['uos']
del sys.modules['networkd']
del sys.modules['flashbdev']

gc.collect()
# python為直譯程式，import即可執行yhttpd(http server)
import yhttpd
gc.collect()
if 'yhttpd' in globals():
    del globals()['yhttpd']
print(gc.mem_free())
