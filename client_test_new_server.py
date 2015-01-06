__author__ = 'xero-mac'
"""
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
"""

# telnet program example
import socket, select, string, sys

def prompt() :
	sys.stdout.write('<You> ')
	sys.stdout.flush()

#main function
if __name__ == "__main__":

	host = "127.0.0.1"
	port = 9999

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	# connect to remote host
	try :
		s.connect((host, port))
	except :
		print 'Unable to connect'
		sys.exit()

	print 'Connected to remote host. Start sending messages'
	prompt()

	while 1:
		socket_list = [sys.stdin, s]

		# Get the list sockets which are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

		for sock in read_sockets:
			#incoming message from remote server
			if sock == s:
				data = sock.recv(4096)
				if not data :
					print '\nDisconnected from chat server'
					sys.exit()
				else :
					#print data
					sys.stdout.write(data)
					prompt()

			#user entered a message
			else :
				msg = sys.stdin.readline()
				s.send(msg)
				prompt()