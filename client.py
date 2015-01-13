'''
    Cloud Computing Project:
    Android Client Monitor
'''
__author__ = 'Peter'
import socket
import sys
import time
import select

LOCAL = socket.gethostbyname(socket.gethostname())

HOST, PORT = LOCAL, 9999
data = " ".join(sys.argv[1:])
user = ""

def prompt():
    sys.stdout.write("<You> ")
    sys.stdout.flush()

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_list = [sys.stdin, sock]

try:
    sock.connect((HOST, PORT))
    print("Welcome to chat room!")

    # Login
    print("[Login]")
    while True:
        i_account = raw_input("Account:")
        i_pwd = raw_input("Password:")
        user_data = "{}/{}/{}".format("login", i_account, i_pwd)
        sock.sendall(user_data)
        received = sock.recv(1024)
        if received == "1":
            print "Authentication valid"
            user = i_account
            break
        elif received == "0":
            print "Invalid Password."
            print "Try again."
        else:
            print received
            print "Try again."

    # Chat
    prompt()
    while True:
        r, w, e = select.select(socket_list, [], [])
        for socket in r:
            if socket == sock:
                data = sock.recv(4096)
                sys.stdout.write(data)  # Waiting for data
                prompt()
            else:
                msg = sys.stdin.readline()
                now = time.localtime()
                send_time = "{}:{}:{}".format(now.tm_hour, now.tm_min, now.tm_sec)
                send_data = "{}/{}/{}".format("chat", user, msg)
                sock.sendall(send_data)
                prompt()

finally:
    sock.close()