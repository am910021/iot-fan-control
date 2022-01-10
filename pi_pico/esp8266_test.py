from machine import UART, Pin
import time
from esp8266 import ESP8266
esp01 = ESP8266()
esp8266_at_ver = None

#print("StartUP",esp01.startUP())
print("ReStart",esp01.reStart())
#print("StartUP",esp01.startUP())
#print("Echo-Off",esp01.echoING())
#print("\r\n\r\n")
'''
Print ESP8266 AT command version and SDK details
'''
esp8266_at_var = esp01.getVersion()
print(esp8266_at_var)

log = esp01.setDefaultWiFiMode(3)
print(log)

log = esp01.setCurrentWiFiMode(3)
print(log)

esp01.createHttpServer('/webpage.html', 80)

def sendHtml(file, pid):
    HTMLFileObject = open (file, "r")
    HTMLFileLines = HTMLFileObject.readlines()
    HTMLFileObject.close()
        
    httpHeader= "HTTP/1.0 200 OK\r\nAccess-Control-Allow-Origin: *\r\nHost:Pico\r\n";
    contentHeader = "Content-type: text/html\r\n\r\n";

    httpHeader='HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nHost:Pico\r\nContent-type: text/html\r\nConnection: close\r\n<!DOCTYPE HTML>'  
    esp01._sendNoRecv('AT+CIPSEND=%d,%d' % (pid, len(httpHeader)+2))
    esp01._sendNoRecv(httpHeader)
    
    #with open(file, "r") as f:
    #    lines = f.readlines()
    #    txt = ''.join(lines)
    #    esp01._sendNoRecv('AT+CIPSEND=%d,%d' % (pid, len(txt)+2))
    #    esp01._sendNoRecv(txt)
    #    esp01._sendNoRecv('AT+CIPCLOSE=%d' % (pid)) # once file sent, close connection
    #    time.sleep(1)
    
    #esp01._sendNoRecv('AT+CIPSEND=%d,25' % (pid))
    #esp01._sendNoRecv('Content-Type: text/html')
    #esp01._sendNoRecv('AT+CIPSEND=%d,19' % (pid))        
    #esp01._sendNoRecv('Connection: close')
    #esp01._sendNoRecv('AT+CIPSEND=%d,2' % (pid))
    #esp01._sendNoRecv('')
    #esp01._sendNoRecv('AT+CIPSEND=%d,17' % (pid))
    #esp01._sendNoRecv('<!DOCTYPE HTML>')
    # After handshake, read in html file from pico and send over serial line by line with CIPSEND
    for line in HTMLFileLines:
        cipsend=line.strip()
        ciplength=len(cipsend)+2 # calculates byte length of send plus newline
        esp01._sendNoRecv('AT+CIPSEND=%d,%d' % (pid, ciplength))
        esp01._sendNoRecv(cipsend)
    time.sleep(0.5)
    esp01._sendNoRecv('AT+CIPCLOSE=%d' % (pid)) # once file sent, close connection
    time.sleep(1)

while True:
    pid = esp01.waitClient()
    sendHtml('/webpage.html', pid)
    pid = esp01.checkClient()
    if pid > -1:
        sendHtml('/webpage.html', pid)