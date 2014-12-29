#!/usr/bin/python
__author__ = 'xero-mac'

import SocketServer
import socket


class TcpHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for Exia-App
    """

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "{} wrote:".format(self.client_address[0])
        print self.data

        # send back upper data
        self.request.sendall(self.data.upper())

if __name__ == "__main__":

    # HOST = socket.gethostbyname(socket.gethostname())
    HOST = "127.0.0.1"
    PORT = 9999

    server = SocketServer.TCPServer((HOST, PORT), TcpHandler)

    server.serve_forever()
