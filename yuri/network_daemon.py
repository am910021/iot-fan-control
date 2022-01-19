import sys, os, time, network
from yuri.sys_config import config as sys_config
from yuri.logger import logger
from yuri.stream_lite import Stream


class NetworkHelper:
    _CLOSED = False

    def __init__(self):
        self.info = {'ap': {}, 'wifi': {}}

    def do_connect(self):
        if NetworkHelper._CLOSED:
            return

        wlan = network.WLAN(network.STA_IF)
        self.info['wifi']['mac'] = (":".join(["%X" % (c) for c in wlan.config('mac')]))

        # 判斷config是否有啟用網路功能
        if not sys_config.wifi['enable']:
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
                    wlan.config('essid') == sys_config.wifi['ssid'] and \
                    wlan.ifconfig()[0] != "0.0.0.0":
                break

            wlan.connect(sys_config.wifi['ssid'], sys_config.wifi['password'])
            time.sleep(5)
            count += 1

        self.info['wifi']['ssid'] = sys_config.wifi['ssid']
        self.info['wifi']['password'] = sys_config.wifi['password']
        self.info['wifi']['ip'] = wlan.ifconfig()[0]
        logger.info('======Connected Info======')
        logger.info('Wi-Fi   ssid ' + self.info['wifi']['ssid'])
        logger.info('Wi-Fi passwd ' + self.info['wifi']['password'])
        logger.info('IP   Address ' + self.info['wifi']['ip'])
        logger.info('MAC  Address ' + self.info['wifi']['mac'])
        logger.info('=========Info End=========')

    def create_ap(self):
        if NetworkHelper._CLOSED:
            return

        ap = network.WLAN(network.AP_IF)  # create access-point interface
        self.info['ap']['mac'] = (":".join(["%X" % (c) for c in ap.config('mac')]))

        if not sys_config.ap['enable']:
            ap.active(False)
            return

        # 如果沒有config.txt檔案，就寫入預設值進config裡
        if sys_config.default_is_loaded:
            ssid = 'IOT-' + ("".join(["%X" % (c) for c in ap.config('mac')[3:]]))

            # 預設的ssid為'iot-<mac_address後三碼>' ex:iot-BE562A
            sys_config.ap['ssid'] = ssid
            # 預設的ssid密碼為'iot-<mac_address後三碼>'的倒置 ex:A265EB-toi
            sys_config.ap['password'] = "".join(ssid[i - 1] for i in range(len(ssid), 0, -1))

            sys_config.http['realm'] = 'ESP_' + ("".join(["%X" % (c) for c in ap.config('mac')]))
            # 預設的http帳號admin
            sys_config.http['user'] = 'admin'
            # 預設的http密碼為預設的ssid密碼
            sys_config.http['password'] = sys_config.ap['password']
            sys_config.save_config()

        # 重啟網路
        if ap.active():
            ap.active(True)

        ap.active(True)  # 啟動網路
        ap.config(essid=sys_config.ap['ssid'], password=sys_config.ap['password'])  # 設定ssid, password
        ap.config(authmode=3)  # 設定驗證模式
        aconfig = ap.ifconfig()

        self.info['ap']['ssid'] = sys_config.ap['ssid']
        self.info['ap']['password'] = sys_config.ap['password']
        self.info['ap']['ip'] = aconfig[0]
        logger.info('======Manage-AP Info======')
        logger.info('AP     ssid ' + self.info['ap']['ssid'])
        logger.info('AP   passwd ' + self.info['ap']['password'])
        logger.info('IP  Address ' + self.info['ap']['ip'])
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
        stream.write_byte(1 if sys_config.ap[enable] else 0)
        if not sys_config.ap[enable]:
            stream.write_str(sys_config.ap[ssid])
            stream.write_str(sys_config.ap[pwd])
            stream.write_str(self.info['ap']['mac'])
        else:
            stream.write_str(self.info['ap'][ssid])
            stream.write_str(self.info['ap'][pwd])
            stream.write_str(self.info['ap']['ip'])
            stream.write_str(self.info['ap']['mac'])

        stream.write_byte(1 if sys_config.wifi[enable] else 0)
        if not sys_config.wifi[enable]:
            stream.write_str(sys_config.wifi[ssid])
            stream.write_str(sys_config.wifi[pwd])
            stream.write_str(self.info['wifi']['mac'])
        else:
            stream.write_str(self.info['wifi'][ssid])
            stream.write_str(self.info['wifi'][pwd])
            stream.write_str(self.info['wifi']['ip'])
            stream.write_str(self.info['wifi']['mac'])

        with open('/tmp/interface.bin', 'wb') as f:
            f.write(stream.get_bytes(True))

    @staticmethod
    def release():
        if NetworkHelper._CLOSED:
            return

        del globals()['Stream']
        del sys.modules['yuri.stream_lite']
        del globals()['logger']
        del sys.modules['yuri.logger']
        del globals()['sys_config']
        del sys.modules['yuri.sys_config']
        del sys.modules['yuri']
        del globals()['network']
        del globals()['time']

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
