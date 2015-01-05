__author__ = 'xero-mac'
""" New Version of Chat Room Server
"""
import socket
import select
import threading
import db
import logging

class ChatRoomServer():
    """ Chat Room Server Class
        Argument:

        - address : A tuple of host and port.

    """
    def __init__(self, address):
        self.connection_list = []
        self.received_buffer = 4096
        self.address = address
        self.request_queue_size = 10
        self.shut_down_request = False
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
                    try:
                        request, client_address = self.get_request()
                    except socket.error:
                        logging.debug("get_request() error.")
                        return

                    # Maybe I should verify the request before going to handle it.
                    self.connection_list.append(request)  # Handle the new connection
                    print "Client {} connected".format(client_address)

                # BroadCast Data!

                else:
                    # Handle request process?
                    pass
        self.server_socket.close()

    def get_request(self):
        return self.server_socket.accept()

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 9999
    server = ChatRoomServer((HOST, PORT))
    server.serve_forever()