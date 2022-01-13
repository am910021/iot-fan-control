import network
import time
# setup as a station
wlan = network.WLAN(mode=WLAN.STA)
wlan.connect('esp8266', auth=(WLAN.WPA2, '0123456789'))
while not wlan.isconnected():
    time.sleep_ms(50)
print(wlan.ifconfig())