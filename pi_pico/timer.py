import time, gc

class Timer:
    def __init__(self, callback, t=1000, *args, **kwargs):
        self._time=t
        self._callback=callback
        self._tmp_time=time.ticks_ms()
        self._args=args
        self._kwargs=kwargs
    
    def tick(self):
        if (time.ticks_ms() - self._tmp_time) > self._time:
            self._callback(*self._args, **self._kwargs)
            self._tmp_time=time.ticks_ms()
        
        