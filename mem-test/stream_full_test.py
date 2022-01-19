import gc, sys
gc.collect()
print(gc.mem_free())
from yuri.stream_full import Stream
gc.collect()
print(gc.mem_free())
