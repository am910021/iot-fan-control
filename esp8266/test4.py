import os, time, gc, network, time
from yuri.stream import Stream
from yuri.logger import logger
from yuri.http.tcpserver import TCPServer
from yuri.http.config import default as default_config
from yuri.http.processor.api import ApiProcess
from yuri.http.processor.file import FileProcess
from yuri.http.handler import my_api, my_api2, api3, network_info, fan_control
from yuri.http.processor import Processor


def do_connect(essid, password):
    gc.collect()
    info = {}
    config = {}
    info['essid'] = essid
    info['password'] = password

    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    # wifis = wlan.scan()  # scan for access points
    count = 0
    while True and count < 10:
        essid_tmp = wlan.config('essid')
        config = wlan.ifconfig()
        # print('isconnected ', wlan.isconnected(), 'essid_tmp ', essid_tmp, '\r\n', config)
        if wlan.isconnected() and essid_tmp == essid:
            break

        tcount = 0
        wlan.connect(essid, password)  # connect to an AP
        while not wlan.isconnected() and tcount < 10:
            time.sleep(1)
            tcount += 1
            # print('waiting wifi connect %d/10' % (tcount))
        count += 1

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
    logger.debug('      Wi-Fi ' + essid)
    logger.debug(' IP Address ' + config[0])
    logger.debug('MAC Address ' + mac)
    logger.debug('=========Info End=========')
    return info


def create_ap(essid, password):
    gc.collect()
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
    logger.debug('Wi-Fi essid ' + essid)
    logger.debug('Wi-Fi   pwd ' + password)
    logger.debug(' IP Address ' + config[0])
    logger.debug('MAC Address ' + mac)
    logger.debug('=========Info End=========')
    return info


def saveInfo(info):
    gc.collect()
    folders = os.listdir()
    if not 'tmp' in folders:
        os.mkdir('/tmp')

    stream = Stream()
    stream.write_str(info['ap']['essid'])
    stream.write_str(info['ap']['password'])
    stream.write_str(info['ap']['ip'])
    stream.write_str(info['ap']['mac'])
    stream.write_str(info['wifi']['essid'])
    stream.write_str(info['wifi']['password'])
    stream.write_str(info['wifi']['ip'])
    stream.write_str(info['wifi']['mac'])

    with open('/tmp/interface.bin', 'wb') as f:
        f.write(stream.get_bytes())


if __name__ == '__main__':
    logger.set_levels([0, 1, 2, 3])
    ap_info = create_ap('esp8266', '0123456789')
    wifi_info = do_connect('Poo_2.4G', '99999990')
    saveInfo({'ap': ap_info, 'wifi': wifi_info})
    gc.collect()

    config = default_config()
    config['port'] = 80
    api_handler = ApiProcess([
        (['test'], my_api.Handler()),
        (['test2'], my_api2.Handler()),
        (['test3'], api3.Handler()),
        (['info'], info.Handler()),
        (['fan'], fan_control.Handler())
    ])

    processor = Processor(handlers=[
        ('/api', api_handler),
        ('/', FileProcess('/www'))
    ], config=config)
    server = TCPServer(processor, config={'address': '0.0.0.0',
                                          'port': 80,
                                          'timeout': 30, })
    server.start()

    # while True:
    #    time.sleep(200 / 1000)
