#!/usr/bin/python2
# -*- coding: utf-8 -*-
__author__ = 'xero-mac'
""" New Version of Chat Room Server
    Using select model to implement the broadcast function
"""
import socket
import select
import threading
import db
import logging
import ChatRoom_handler


class ChatRoomServer():
    """ Chat Room Server Class
        Argument:

        - address : A tuple of host and port.

    """
    def __init__(self, address, RequestHandlerClass):
        self.connection_list = []
        self.received_buffer = 4096
        self.address = address
        self.RequestHandlerClass = RequestHandlerClass
        self.request_queue_size = 10
        self.shut_down_request = False
        self.daemon_threads = False
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.build_server()

    def build_server(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.address)
        self.server_socket.listen(self.request_queue_size)
        self.connection_list.append(self.server_socket)
        logging.debug("Server start at {}", self.address)
        print "Chat Room Start at {}".format(self.address)

    def serve_forever(self):
        while not self.shut_down_request:
            r, w, e = select.select(self.connection_list, [], [])

            for sock in r:
                if sock == self.server_socket:
                    print "New connection sock in r"
                    try:
                        request, client_address = self.get_request()
                    except socket.error:
                        logging.debug("get_request() error.")
                        return

                    # Maybe I should verify the request before going to handle it.
                    self.connection_list.append(request)  # Handle the new connection
                    print "Client {} connected".format(client_address)

                # BroadCast Data!
                    self.broadcast_data(request, "{} entered room\n".format(client_address))

                else:
                    print "Old socket in r ?"
                    # Handle request process, write thread here?
                    try:
                        request, client_address = self.get_request()
                    except socket.error:
                        return

                    if self.verify_request(request, client_address):
                        try:
                            self.process_request(request, client_address)
                        except:
                            logging.debug("process_request error")

        self.server_socket.close()

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self)

    def process_request_thread(self, request, client_address):
        """Handle one request thread
        """
        try:
            self.finish_request(request, client_address)
        except:
            #  maybe writing a shut down request method here.
            pass

    def process_request(self, request, client_address):
        """Init thread of request
        """
        t = threading.Thread(target=self.process_request_thread,
                             args=(request, client_address))
        t.daemon = self.daemon_threads
        t.start()

    def verify_request(self, request, client_address):
        return True

    def broadcast_data(self, sock, message):
        for socket in self.connection_list:
            if socket != self.server_socket and socket != sock:
                try:
                    socket.send(message)
                except:
                    #  Can't broadcast message to this socket, maybe it has been shut down.
                    socket.close()
                    self.connection_list.remove(socket)

    def get_request(self):
        return self.server_socket.accept()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 9999
    server = ChatRoomServer((HOST, PORT), ChatRoom_handler.ChatRoomHandler)
    server.serve_forever()