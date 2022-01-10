import gc, sys
import os
import time
import network
from yuri.config import config as gConfig
from yuri.logger import logger
from yuri.stream import Stream

class NetworkHelper:
    _CLOSED=False
    
    def __init__(self):
        self.info ={}
        self.info['ap'] ={}
        self.info['wifi'] ={}

    def doConnect(self):
        if not gConfig.wifi['enable'] or NetworkHelper._CLOSED:
            return

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)

        count=0
        while True and count < 10:
            essid_tmp=wlan.config('essid')
            wconfig = wlan.ifconfig()
            if wlan.isconnected() and essid_tmp == gConfig.wifi['essid']:
                break

            tcount=0
            wlan.connect(gConfig.wifi['essid'], gConfig.wifi['password'])
            while not wlan.isconnected() and tcount < 10:
                time.sleep(1)
                tcount+=1
            count+=1

        wconfig = wlan.ifconfig()
        if wconfig[0] == "0.0.0.0":
            time.sleep(5)
            wconfig = wlan.ifconfig()
            
       
        self.info['wifi']['essid'] = gConfig.ap['essid']
        self.info['wifi']['password'] = gConfig.ap['password']
        self.info['wifi']['ip'] = wconfig[0]
        self.info['wifi']['mac'] = (":".join(["%X" % (c) for c in wlan.config('mac')]))

        logger.debug('======Connected Info======')
        logger.debug('      Wi-Fi '+ self.info['wifi']['essid'])
        logger.debug(' IP Address '+ self.info['wifi']['ip'])
        logger.debug('MAC Address '+ self.info['wifi']['mac'])
        logger.debug('=========Info End=========')


    def createAP(self):
        if NetworkHelper._CLOSED:
            return
        
        ap = network.WLAN(network.AP_IF)  # create access-point interface
        ap.active(True)  # activate the interface
        ap.config(essid=gConfig.ap['essid'], password=gConfig.ap['password'], channel=5)  # set the ESSID of the access point
        mac_bytes = ap.config('mac')
        mac = (":".join(["%X" % (c) for c in mac_bytes]))
        aconfig = ap.ifconfig()

        self.info['ap']['essid'] = gConfig.ap['essid']
        self.info['ap']['password'] = gConfig.ap['password']
        self.info['ap']['ip'] = aconfig[0]
        self.info['ap']['mac'] = mac

        logger.debug('======Manage-AP Info======')
        logger.debug('Wi-Fi essid '+ self.info['ap']['essid'])
        logger.debug('Wi-Fi   pwd '+ self.info['ap']['password'])
        logger.debug(' IP Address '+ self.info['ap']['ip'])
        logger.debug('MAC Address '+ self.info['ap']['mac'])
        logger.debug('=========Info End=========')


    def saveInfo(self):
        if NetworkHelper._CLOSED:
            return
        
        folders = os.listdir()
        if not 'tmp' in folders:
            os.mkdir('/tmp')

        stream = Stream()
        stream.writeStr(self.info['ap']['essid'])
        stream.writeStr(self.info['ap']['password'])
        stream.writeStr(self.info['ap']['ip'])
        stream.writeStr(self.info['ap']['mac'])
        stream.writeStr(self.info['wifi']['essid'])
        stream.writeStr(self.info['wifi']['password'])
        stream.writeStr(self.info['wifi']['ip'])
        stream.writeStr(self.info['wifi']['mac'])

        with open('/tmp/interface.bin', 'wb') as f:
            f.write(stream.getBytes())
            
    @staticmethod
    def release():
        if NetworkHelper._CLOSED:
            return

        del globals()['Stream']
        del sys.modules['yuri.stream']
        del globals()['logger']
        del sys.modules['yuri.logger']
        del globals()['gConfig']
        del sys.modules['yuri.config']
        del sys.modules['yuri']
        del globals()['network']
        del globals()['time']
        del globals()['os']
        del globals()['sys']
        del globals()['gc']
        
        NetworkHelper._CLOSED=True

'''
if __name__ == '__main__':
    print(gConfig.ap)
    networkd = NetworkHelper()
    networkd.doConnect()
    networkd.createAP()
    networkd.saveInfo()
    #print(sys.modules)
    #print(8,gc.mem_free())
    #networkd.close()
    #del Stream
    #del sys.modules['yuri.stream']
    #del logger
    #del sys.modules['yuri.logger']
    #del config
    #del sys.modules['yuri.config']
    #del sys.modules['yuri']
    #del network
    #del time
    #del os

    gc.collect()

    print(9,gc.mem_free())
    print(sys.modules)
'''