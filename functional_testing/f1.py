import gc, sys

gc.collect()
print(gc.mem_free())
gc.collect()

UART = getattr(__import__('machine'), 'UART')
uart = UART(2, baudrate=115200, tx=17, rx=16, txbuf=256, rxbuf=256)
gc.collect()
print(gc.mem_free())