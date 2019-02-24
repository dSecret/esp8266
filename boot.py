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

class RoomLight:

    def __init__(self):
        
        self.state = "off"
        self.pin = machine.Pin(2,machine.Pin.OUT)

    def setState(self, val):

        print("Changed state to {}".format(val))
        self.state = val
        self.action()

    def action(self):

        if self.state == "off":
            self.pin.value(0)
        elif self.state == "on":
            self.pin.value(1)
        else:
            pass

    def handleRequest(self, request):

        req = str(request)
        if req.find("/turnon") >= 0:
            self.setState("on")
        if req.find("/turnoff") >= 0:
            self.setState("off")
        else:
            pass

    def serveHTML(self):

        return """<!DOCTYPE html>
        <html>
            <head>
                <title>Room Light</title>
                <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                <style>
                    .off {
                        background-color: black;
                        color: white;
                    }
                    .on {
                        background-color: white;
                        color: black;
                    }
                </style>
            </head>""" + """
            <body class="{state}">
                <div class="container">
                    <h1 class="{state}" style="text-align: center;">The lights are {state} currently</h1>
                    <form action="/turn{otherState}" method="get">
                        <button type="submit" class="btn btn-outline-secondary">Turn {otherState}</button>
                    </form>
                </div>
            </body>
        </html>
        """.format(state=self.state, otherState="off" if self.state == "on" else "on")



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

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

rl = RoomLight()

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

        # handlePin(val)
        rl.handleRequest(val)
        cl.send(rl.serveHTML())
        cl.send("\r\n")
        cl.close()
