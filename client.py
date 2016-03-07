import json


import socket
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 6969
BUFFER_SIZE = 1024
# MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        print 'connecting...',
        s.connect((TCP_IP, TCP_PORT))
        print 'ok'
        
        try:
            while True:
                data = s.recv(BUFFER_SIZE)
                print "received data:", data
                if not data: break

        except socket.error, e:
            print 'socket error', e
        finally:
            s.close()
    except socket.error:
        print ''
        time.sleep(1)
