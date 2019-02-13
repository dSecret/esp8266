# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import network
import socket

webrepl.start()
gc.collect()

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('rush_b', 'rushrushB')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()

pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>ESP8266 Pins</h1>
        
    </body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

def handlePin(val):
	val = str(val)
	pin = machine.Pin(2,machine.Pin.OUT)
        foo = val.find('?search=')
        print(val)
        if foo >=0:
	    if val[15]=="2":
		pin.value(0)
	    else:
		pin.value(1)


while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        val = ""
        i=0
        while True:
            line = cl_file.readline()
            if i==0 :
                val +=str(line)
            i = i+1
            if not line or line == b'\r\n':
                break
        handlePin(val)
        cl.send(html)
        cl.close()
