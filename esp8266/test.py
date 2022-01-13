import network, time

def doConnect(essid, password):
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wifis = wlan.scan()             # scan for access points
    if not wlan.isconnected():
          # check if the station is connected to an AP
        wlan.connect(essid, password) # connect to an AP
        time.sleep(1)

    essid=wlan.config('essid')
    mac_bytes=wlan.config('mac')
    mac=(":".join(["%X" % (c) for c in mac_bytes]))
    config=wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses
    print(config)
    print('======Connected Info======')
    print('      Wi-Fi ',essid,'\r\n IP Address ', config[0], '\r\nMAC Address ', mac)
    print('=========Info End=========')

def createAP(essid, password):
    ap = network.WLAN(network.AP_IF) # create access-point interface
    ap.active(True)         # activate the interface
    ap.config(essid=essid, password=password, channel=5) # set the ESSID of the access point
    time.sleep(1)
    
    mac_bytes=ap.config('mac')
    mac=(":".join(["%X" % (c) for c in mac_bytes]))
    config = ap.ifconfig()
    print(config)
    print('======Manage-AP Info======')
    print('Wi-Fi essid ', essid)
    print('Wi-Fi   pwd ', password)
    print(' IP Address ', config[0])
    print('MAC Address ', mac)
    print('=========Info End=========')



if __name__ == '__main__':
    doConnect('Poo_2.4G', '99999990')
    createAP('esp8266', '0123456789')