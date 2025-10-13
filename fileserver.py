import socket
import threading
import os
import getpass

host = '127.0.0.1'
port = 55557
admin_pass='qwerty'

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(1)

clients=[]
usernames=[]
def authenticate_admin():
    passAttempt=getpass.getpass("Enter Admin password: ")
    if passAttempt==admin_pass:
        return True
    else:
        return False
def authenticate_client(clientUsername,clientPassword):
    with open('~/Documents/pass.txt','r') as file:
        for line in file:
            line.strip()
            if '=' in line:
                Susername,Spassword = line.split('=',1)
                username=Susername.strip()
                password=Spassword.strip()
            if clientUsername==username and clientPassword==password:
                return True
            else:
                return False


def handle_clients():
    while True:
        client,address=server.accept()
        client.send("UN".encode('ascii'))
        clientUsername=client.recv(1024).decode('ascii')
        client.send("PASS ".encode('ascii'))
        clientPassword=client.recv(1024).decode('ascii')
        if authenticate_client(clientUsername,clientPassword):
            print("Client authenticated ")
            client.send("Authentication Success".encode('ascii'))
            clients.append(client)
            usernames.append(clientUsername)
            server.close()

        else:
            print("Client authentication failed")
            client.send("Authentication failed".encode('ascii'))
            client.close()
            break

        handleThread=threading.Thread(target=handle_clients)
        handleThread.start()

def server_handle():
    if authenticate_admin():
        while True:
            server_input=input("> ")

            if server_input =='PWD':
                print(os.getcwd())
            elif server_input=='LIST':
                print(os.listdir())
            elif server_input=='CLIENT':
                print(f"{clients[0]}:{usernames[0]}")
            elif server_input == 'DELETE':
                rmFile=input("> Name of the file >> ")
                try:
                    os.remove(rmFile)
                    print(f"{rmFile} is removed")

                except FileNotFoundError:
                    print(f"Error: {rmFile} does not exist")

                    
    else:
        print("Authentication failed")
    
    server_handle_thread=threading.Thread(target=server_handle)
    server_handle_thread.start()

def receive():