import os, gc, sys, time


# 倒數10秒，在10秒期間repl還可以作用
start = time.ticks_ms()
countdown = 10
while (time.ticks_ms() - start) < (countdown * 1000):
    print('%d seconds left for repl to detach from uart0.' % (countdown - round((time.ticks_ms() - start) / 1000)))
    time.sleep(1)

# 關閉esp8266的repl釋放uart0
os.dupterm(None, 1)
del globals()['start']
del globals()['countdown']
del globals()['time']

# python為直譯程式，import即可執行networkd
import networkd

# 移除除執行過的網路連線程式networkd

del globals()['bdev']
del globals()['networkd']
del sys.modules['networkd']
del sys.modules['flashbdev']
gc.collect()
# python為直譯程式，import即可執行yhttpd(http server)
import yhttpd
gc.collect()
if 'yhttpd' in globals():
    del globals()['yhttpd']
print(gc.mem_free())
