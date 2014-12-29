'''
    Cloud Computing Project:
    This is the server for the android communicate application.

    The socket data type is [Command | DATA|]

'''

__author__ = 'xero7689'

import SocketServer
import threading
import socket
import db

def wrap_socket_data(*args):
    wrapdata = '/'.join(args)
    return wrapdata

database = "Exia.db"


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    """ Threaded Tcp Request Handler class

    This class is going to be passed into ThreadedTcpServer as a parameter.


    """

    def init_function(self):
        self.db = db.ChatDB(database)
        self.user = None
        self.functionDict = {'1': self.signup,
                             '2': self.log_in,
                             '3': self.client_talk,
                             }

    def signup(self, data):
        try:
            print "{}-{}".format(data[0], data[1])
            print "is asking to sign up."
            if self.db.add_new_user(data[0], data[1]) is False:
                self.request.sendall("[Register]Fail!")
            else:
                print "[Regist]-{}-{}".format(data[0], data[1])
                self.request.sendall("[Register]Done!")
        except:
            print "An error occurred while account registering."

    def log_in(self, data):
        flag = self.db.check_account(data[0], data[1])
        if flag is True:
            self.request.sendall("valid")
            self.user = data[0]
        elif flag is False:
            self.request.sendall("invalid")  # Error password
        else:
            self.request.sendall(flag)  # Account doesn't exist

    def client_talk(self, data):
        #  data[0] = time, data[1] = msg
        try:
            self.db.add_new_post(self.user, data[0], data[1])
            print "[Client][{}]{}: {}".format(data[0], self.user, data[1])
            self.request.sendall("[Server]: {}".format(data[1]))
        except:
            print "[Error]: client_talk"

    def update_client(self):
        pass

    def handle(self):
        self.init_function()

        while True:
            received_data = self.request.recv(1024).strip()
            cur_thread = threading.currentThread()

            received_data_list = received_data.split("/")
            command = received_data_list[0]
            data = received_data_list[1:]

            print "[{}]:".format(cur_thread)
            self.functionDict[command](data)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def server_bind(self):
        # Avoid address already in use error
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

if __name__ == "__main__":
    # HOST = socket.gethostbyname(socket.gethostname())
    HOST = "127.0.0.1"
    PORT = 9999

    # Init the database

    # Create the server, binding to localhost on port 9999.
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.serve_forever()

    print "Server loop running in thread:", server.thread.name