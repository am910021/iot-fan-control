import os, time

start = time.ticks_ms()
countdown = 10
while (time.ticks_ms() - start) < (countdown * 1000):
    print('%d seconds left for repl to detach from uart0.' % (countdown - round((time.ticks_ms() - start) / 1000)))
    time.sleep(1)

#os.dupterm(None, 1)
del globals()['start']
del globals()['countdown']
del globals()['time']