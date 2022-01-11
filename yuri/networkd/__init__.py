import gc, sys, os, time, network
from ..config import config as gConfig
from yuri.logger import logger
from yuri.stream import Stream


class NetworkHelper:
    _CLOSED = False

    def __init__(self):
        self.info = {}
        self.info['ap'] = {}
        self.info['wifi'] = {}

    def do_connect(self):
        if NetworkHelper._CLOSED:
            return

        wlan = network.WLAN(network.STA_IF)

        # 判斷config是否有啟用網路功能
        if not gConfig.wifi['enable']:
            wlan.active(False)
            return

        # 重啟網路
        if wlan.active():
            wlan.active(True)

        wlan.active(True)

        # 嚐試連線到wifi直到連上or試過10次
        count = 0
        while True and count < 10:
            if wlan.isconnected() and \
                    wlan.config('essid') == gConfig.wifi['ssid'] and \
                    wlan.ifconfig()[0] != "0.0.0.0":
                break

            wlan.connect(gConfig.wifi['ssid'], gConfig.wifi['password'])
            time.sleep(5)
            count += 1

        self.info['wifi']['ssid'] = gConfig.ap['ssid']
        self.info['wifi']['password'] = gConfig.ap['password']
        self.info['wifi']['ip'] = wlan.ifconfig()[0]
        self.info['wifi']['mac'] = (":".join(["%X" % (c) for c in wlan.config('mac')]))

        logger.info('======Connected Info======')
        logger.info('      Wi-Fi ' + self.info['wifi']['ssid'])
        logger.info(' IP Address ' + self.info['wifi']['ip'])
        logger.info('MAC Address ' + self.info['wifi']['mac'])
        logger.info('=========Info End=========')

    def create_ap(self):
        if NetworkHelper._CLOSED:
            return

        ap = network.WLAN(network.AP_IF)  # create access-point interface
        if not gConfig.ap['enable']:
            ap.active(False)
            return

        # 如果沒有config.txt檔案，就寫入預設值進config裡
        if gConfig.default_is_loaded:
            ssid = 'IOT-'+("".join(["%X" % (c) for c in ap.config('mac')[3:]]))

            # 預設的ssid為'iot-<mac_address後三碼>' ex:iot-BE562A
            gConfig.ap['ssid']=ssid
            # 預設的ssid密碼為'iot-<mac_address後三碼>'的倒置 ex:A265EB-toi
            gConfig.ap['password'] = "".join(ssid[i-1] for i in range(len(ssid), 0, -1))

            gConfig.http['realm'] = 'ESP_'+("".join(["%X" % (c) for c in ap.config('mac')]))
            # 預設的http帳號admin
            gConfig.http['user'] = 'admin'
            # 預設的http密碼為預設的ssid密碼
            gConfig.http['password'] = gConfig.ap['password']
            gConfig.save_config()

        # 重啟網路
        if ap.active():
            ap.active(True)

        ap.active(True)  # 啟動網路
        ap.config(essid=gConfig.ap['ssid'], password=gConfig.ap['password']) # 設定ssid, password
        ap.config(authmode=3)  # 設定驗證模式
        mac_bytes = ap.config('mac')
        mac = (":".join(["%X" % (c) for c in mac_bytes]))
        aconfig = ap.ifconfig()

        self.info['ap']['ssid'] = gConfig.ap['ssid']
        self.info['ap']['password'] = gConfig.ap['password']
        self.info['ap']['ip'] = aconfig[0]
        self.info['ap']['mac'] = mac
        logger.info('======Manage-AP Info======')
        logger.info('Wi-Fi ssid ' + self.info['ap']['ssid'])
        logger.info('Wi-Fi   pwd ' + self.info['ap']['password'])
        logger.info(' IP Address ' + self.info['ap']['ip'])
        logger.info('MAC Address ' + self.info['ap']['mac'])
        logger.info('=========Info End=========')

    def save_info(self):
        if NetworkHelper._CLOSED:
            return

        folders = os.listdir()
        if 'tmp' not in folders:
            os.mkdir('/tmp')

        stream = Stream()
        stream.writeStr(self.info['ap']['ssid'])
        stream.writeStr(self.info['ap']['password'])
        stream.writeStr(self.info['ap']['ip'])
        stream.writeStr(self.info['ap']['mac'])
        if gConfig.wifi['enable']:
            stream.writeStr(self.info['wifi']['ssid'])
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

        NetworkHelper._CLOSED = True


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