__author__ = 'xero-mac'

import socket
import select
import sys

HOST = "127.0.0.1"
PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    print "Connect!"
    sock_list = []
    sock_list.append(sock)
    sock_list.append(sys.stdin)

    print "->"
    while True:
        r, w, e = select.select(sock_list, [], [])

        for socket in r:
            if socket == sock:
                recv = sock.recv(1024)
                if not recv:
                    break
                else:
                    print recv
            else:
                msg = sys.stdin.readline()
                sock.send(msg)
                print "->"

except:
    print "error!"