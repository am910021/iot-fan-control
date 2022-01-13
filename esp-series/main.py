import gc, sys

# python為直譯程式，import即可執行networkd
import networkd

# 移除除執行過的網路連線程式networkd
if 'networkd' in globals():
    del globals()['networkd']
if 'networkd' in sys.modules:
    del sys.modules['networkd']



gc.collect()
# python為直譯程式，import即可執行yhttpd(http server)
import yhttpd
print(gc.mem_free())

if 'yhttpd' in globals():
    del globals()['yhttpd']
if 'flashbdev' in sys.modules:
    del sys.modules['flashbdev']
print(gc.mem_free())
