import time

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
            
#def test(a, b,c,d):
#    print('test', a, b,c,d)
            
            
#if __name__ == '__main__':
#    tt = Timer(test, 1000, [0,1,2,3],{'2':2}, [4,5,6,7], {'1':1})
#    while True:
#        tt.tick()
#        time.sleep(0.2)
#        print(1)
        
        