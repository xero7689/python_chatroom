__author__ = 'xero-mac'

import threading

class ChatRoomHandler():
    """ Handler for chat room
    """
    def __init__(self, request, client_address, target_server):
        self.request = request
        self.client_address = client_address
        self.server = target_server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        """For Debug
        """
        cur_thread = threading.currentThread()
        print "Thread start at {}".format(cur_thread)

        while True:
            received_data = self.request.recv(1024).strip()
            print "{} wrote:".format(self.client_address)
            print received_data

            for socket in self.server.connection_list:
                if socket != self.server.server_socket and socket != self.request:
                    try:
                        socket.send(received_data)
                    except:
                        socket.close()
                        self.server.connection_list.remove(socket)

            self.request.sendall("Got your data")

    def finish(self):
        pass

