import gc, sys, time, os
from yuri.NetworkHelper import NetworkHelper

from uhttpd.uhttpd import Server
from uhttpd import http_file_handler, http_api_handler
import info, fan_control
from yuri.stream import Stream
from yuri.timer import Timer
from yuri.uart_write import uart
from yuri.config import config
from yuri.logger import logger

print(gc.mem_free())

#Release the memory used from this file, including the imported module.
def close():
    del globals()['NetworkHelper']
    del sys.modules['yuri.NetworkHelper']
    if 'network' in globals():
        del globals()['network']
    if 'yuri' in globals():
        del globals()['yuri']

def createWWW():
    folders = os.listdir()
    if not 'www' in folders:
        os.mkdir('/www')
        f = open('/www/index.html', 'w')
        f.write('<html><body>Hello World!</body></html>')
        f.close()
        os.listdir('/www')
        #print('www folder created, index.html created!')
    else:
        #print('www folder is exists.')
        pass

def startServer():
    gc.collect()
    print(gc.mem_free())
    
    api_handler = http_api_handler.Handler([
        #(['test'], my_api.Handler()),
        #(['test2'], my_api2.Handler()),
        #(['test3'], api3.Handler()),
        (['info'], info.Handler()),
        (['fan'], fan_control.Handler())
    ])
    print(gc.mem_free())
    server = Server(config={
        'bind_addr': '0.0.0.0',
        'port': 80,
        'timeout': 15,
        'require_auth': False,
        'realm': "esp8266",
        'user': "admin",
        'password': "uhttpD",
        'max_headers': 10,
        'max_content_length': 1024,
        # NB. SSL currently broken
        'use_ssl': False,
        'dev': True
    }, handlers=[
        ('/api', api_handler),
        ('/', http_file_handler.Handler('/www'))
    ])
    server.start()

def sendLiveSingle():
    stream = Stream()
    stream.write_byte(0)
    uart.write(stream.get_bytes())

if __name__ == '__main__':
    logger.set_levels([0, 1, 2, 3])
    #enable network ap / wifi.
    network = NetworkHelper()
    network.do_connect()
    network.create_ap()
    network.save_info()
    NetworkHelper.release() #release used memory.
    print(gc.mem_free())
    close()
    time.sleep(1)
    gc.collect()
    time.sleep(1)
    
    
    sconfig = config.http
    sconfig['use_ssl']=False,
    sconfig['dev']= True
    print(gc.mem_free())
    createWWW()
    print(gc.mem_free())
    time.sleep(1)
    gc.collect()
    print(gc.mem_free())
    startServer()
    print(gc.mem_free())
    tt = Timer(gc.collect, 1000*60)
    live=Timer(sendLiveSingle, 1000*30)
    #while True:
    #    live.tick()
    #    tt.tick()
    #    print(gc.mem_free(), sys.modules)
    #    time.sleep(200 / 1000)