import socket
import threading
host="127.0.0.1"
port=55556
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

def receive():
    