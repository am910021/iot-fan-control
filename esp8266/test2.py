import os, time, gc, network, time
from uhttpd.uhttpd import Server
from uhttpd import http_file_handler, http_api_handler
from uhttpd.demo import my_api, my_api2
import api3, info, fan_control
from yuri.stream import Stream
from yuri.timer import Timer
from yuri.uart_write import uart
from yuri.logger import logger

def doConnect(essid, password):
    info = {}
    info['essid'] = essid
    info['password'] = password

    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    # wifis = wlan.scan()  # scan for access points
    count=0
    while True and count < 10:
        essid_tmp=wlan.config('essid')
        config = wlan.ifconfig()
        #print('isconnected ', wlan.isconnected(), 'essid_tmp ', essid_tmp, '\r\n', config)
        if wlan.isconnected() and essid_tmp == essid:
            break

        tcount=0
        wlan.connect(essid, password)  # connect to an AP
        while not wlan.isconnected() and tcount < 10:
            time.sleep(1)
            tcount+=1
            #print('waiting wifi connect %d/10' % (tcount))
        count+=1

    config = wlan.ifconfig()
    if config[0] == "0.0.0.0":
        time.sleep(5)
        config = wlan.ifconfig()
    essid = wlan.config('essid')
    mac_bytes = wlan.config('mac')
    mac = (":".join(["%X" % (c) for c in mac_bytes]))
    info['mac'] = mac
    info['ip'] = config[0]

    logger.debug('======Connected Info======')
    logger.debug('      Wi-Fi '+ essid)
    logger.debug(' IP Address '+ config[0])
    logger.debug('MAC Address '+ mac)
    logger.debug('=========Info End=========')
    return info


def createAP(essid, password):
    info = {}
    ap = network.WLAN(network.AP_IF)  # create access-point interface
    ap.active(True)  # activate the interface
    ap.config(essid=essid, password=password, channel=5)  # set the ESSID of the access point
    mac_bytes = ap.config('mac')
    mac = (":".join(["%X" % (c) for c in mac_bytes]))
    config = ap.ifconfig()

    info['essid'] = essid
    info['password'] = password
    info['ip'] = config[0]
    info['mac'] = mac

    logger.debug('======Manage-AP Info======')
    logger.debug('Wi-Fi essid '+ essid)
    logger.debug('Wi-Fi   pwd '+ password)
    logger.debug(' IP Address '+ config[0])
    logger.debug('MAC Address '+ mac)
    logger.debug('=========Info End=========')
    return info


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


def saveInfo(info):
    folders = os.listdir()
    if not 'tmp' in folders:
        os.mkdir('/tmp')

    stream = Stream()
    stream.writeStr(info['ap']['essid'])
    stream.writeStr(info['ap']['password'])
    stream.writeStr(info['ap']['ip'])
    stream.writeStr(info['ap']['mac'])
    stream.writeStr(info['wifi']['essid'])
    stream.writeStr(info['wifi']['password'])
    stream.writeStr(info['wifi']['ip'])
    stream.writeStr(info['wifi']['mac'])

    with open('/tmp/interface.bin', 'wb') as f:
        f.write(stream.getBytes())

        

def startServer(config):
    api_handler = http_api_handler.Handler([
        (['test'], my_api.Handler()),
        (['test2'], my_api2.Handler()),
        (['test3'], api3.Handler()),
        (['info'], info.Handler()),
        (['fan'], fan_control.Handler())
    ])
    print(gc.mem_free())
    server = Server(config=config, handlers=[
        ('/api', api_handler),
        ('/', http_file_handler.Handler('/www'))
    ])
    server.start()

def sendLiveSingle():
    stream = Stream()
    stream.writeByte(0)
    uart.write(stream.getBytes())

if __name__ == '__main__':
    gc.collect()
    config = {
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
    }
    logger.setLevels([1, 3])
    ap_info = createAP('esp8266', '0123456789')
    gc.collect()
    wifi_info = doConnect('Poo_2.4G', '99999990')
    gc.collect()
    createWWW()
    saveInfo({'ap': ap_info, 'wifi': wifi_info})
    gc.collect()
    startServer(config)
    # startServerApi(config)
    
    tt = Timer(gc.collect, 1000*60)
    live=Timer(sendLiveSingle, 1000*30)
    while True:
        live.tick()
        tt.tick()
        time.sleep(200 / 1000)