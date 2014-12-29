'''
    Cloud Computing Project:
    Android Client Monitor
'''
__author__ = 'Peter'
import socket
import sys
import time

LOCAL = "127.0.0.1"

HOST, PORT = LOCAL, 9999
data = " ".join(sys.argv[1:])


# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    print("Welcome to chat room!")

    # Login
    print("[Login]")
    while True:
        i_account = raw_input("Account:")
        i_pwd = raw_input("Password:")
        user_data = "{}/{}/{}".format(2, i_account, i_pwd)
        sock.sendall(user_data)
        received = sock.recv(1024)
        if received is "valid":
            print "Authentication valid"
            break
        elif received is "invalid":
            print "Invalid Password"
            print "Try again.."
        else:
            print received
            print "Try again.."

    # Chating
    while True:
        clinet_msg = raw_input("{}: ".format(i_account))
        if clinet_msg is "":
            print "Stop chating.."
            break
        send_time = time.ctime()
        send_data = "{}/{}/{}".format(3, send_time, clinet_msg)

finally:
    sock.close()