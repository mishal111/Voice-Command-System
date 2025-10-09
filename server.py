import threading
import socket

host = "127.0.0.1"
port = 55556 

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.receive(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            client.close()
            clients.remove(client)
            nicknames.remove(index)
            broadcast(f"The {nickname} is left the chat".encode('ascii')) 
            break

def receive():
    client,address = server.accept()
    clients.append(client)
    print(f""+(str(address))+"joined the chat")
    client.send("Enter your nickname: ".encode(ascii))
    nickname=client.receive()
    nicknames.append(nickname)
    print(f"Nickname of client "+(nickname))
    broadcast(f"{nickname} has joined the chat")
    client.send("You are joined the chatroom".encode(ascii))
    thread=threading.Thread(target=handle, args=client,)
    thread.start()

print(f"Server is listening on {host}:{port}")
receive()
