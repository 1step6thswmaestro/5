import socket
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP: ", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
a=int( sys.argv[1])

while a:
    a -=1
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto( MESSAGE, ( UDP_IP, UDP_PORT))
