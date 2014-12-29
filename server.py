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

def wrapSocketData(*args):
    wrapData = '/'.join(args)
    return wrapData

database = "Exia.db"

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def initfunction(self):
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
                self.request.sendall("[Regist]Fail!")
            else:
                print "[Regist]-{}-{}".format(data[0], data[1])
                self.request.sendall("[Regist]Done!")
        except:
            print "An error occured while regist account."

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
            self.db.add_new_post(self.user, data[1])
        except:
            print "[Error]: client_talk"

    def update_client(self):
        pass

    def handle(self):
        self.initfunction()

        recvData = self.request.recv(1024).strip()
        cur_thread = threading.currentThread()

        recvDataList = recvData.split("/")
        command = recvDataList[0]
        data = recvDataList[1:]

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