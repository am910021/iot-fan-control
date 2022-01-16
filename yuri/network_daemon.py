import sys, os, time, network
from .sys_config import config as sys_onfig
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
        if not sys_onfig.wifi['enable']:
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
                    wlan.config('essid') == sys_onfig.wifi['ssid'] and \
                    wlan.ifconfig()[0] != "0.0.0.0":
                break

            wlan.connect(sys_onfig.wifi['ssid'], sys_onfig.wifi['password'])
            time.sleep(5)
            count += 1

        self.info['wifi']['ssid'] = sys_onfig.wifi['ssid']
        self.info['wifi']['password'] = sys_onfig.wifi['password']
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
        if not sys_onfig.ap['enable']:
            ap.active(False)
            return

        # 如果沒有config.txt檔案，就寫入預設值進config裡
        if sys_onfig.default_is_loaded:
            ssid = 'IOT-' + ("".join(["%X" % (c) for c in ap.config('mac')[3:]]))

            # 預設的ssid為'iot-<mac_address後三碼>' ex:iot-BE562A
            sys_onfig.ap['ssid'] = ssid
            # 預設的ssid密碼為'iot-<mac_address後三碼>'的倒置 ex:A265EB-toi
            sys_onfig.ap['password'] = "".join(ssid[i - 1] for i in range(len(ssid), 0, -1))

            sys_onfig.http['realm'] = 'ESP_' + ("".join(["%X" % (c) for c in ap.config('mac')]))
            # 預設的http帳號admin
            sys_onfig.http['user'] = 'admin'
            # 預設的http密碼為預設的ssid密碼
            sys_onfig.http['password'] = sys_onfig.ap['password']
            sys_onfig.save_config()

        # 重啟網路
        if ap.active():
            ap.active(True)

        ap.active(True)  # 啟動網路
        ap.config(essid=sys_onfig.ap['ssid'], password=sys_onfig.ap['password'])  # 設定ssid, password
        ap.config(authmode=3)  # 設定驗證模式
        mac_bytes = ap.config('mac')
        mac = (":".join(["%X" % (c) for c in mac_bytes]))
        aconfig = ap.ifconfig()

        self.info['ap']['ssid'] = sys_onfig.ap['ssid']
        self.info['ap']['password'] = sys_onfig.ap['password']
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

        enable = 'enable'
        ssid = 'ssid'
        pwd = 'password'
        stream = Stream()
        stream.write_bool(sys_onfig.ap[enable])
        if not sys_onfig.ap[enable]:
            stream.write_str(sys_onfig.ap[ssid])
            stream.write_str(sys_onfig.ap[pwd])
        else:
            stream.write_str(self.info['ap'][ssid])
            stream.write_str(self.info['ap'][pwd])
            stream.write_str(self.info['ap']['ip'])
            stream.write_str(self.info['ap']['mac'])

        stream.write_bool(sys_onfig.wifi[enable])
        if not sys_onfig.wifi[enable]:
            stream.write_str(sys_onfig.wifi[ssid])
            stream.write_str(sys_onfig.wifi[pwd])
        else:
            stream.write_str(self.info['wifi'][ssid])
            stream.write_str(self.info['wifi'][pwd])
            stream.write_str(self.info['wifi']['ip'])
            stream.write_str(self.info['wifi']['mac'])

        with open('/tmp/interface.bin', 'wb') as f:
            f.write(stream.get_bytes())

    @staticmethod
    def release():
        if NetworkHelper._CLOSED:
            return

        del globals()['Stream']
        del sys.modules['yuri.stream']
        del globals()['logger']
        del sys.modules['yuri.logger']
        del sys.modules['yuri.sys_config']
        del sys.modules['yuri']
        del globals()['network']
        del globals()['time']
        del globals()['os']
        del globals()['sys']

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
