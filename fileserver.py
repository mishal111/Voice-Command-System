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
        client.send("UN".encode())
        clientUsername=client.recv(1024).decode()
        client.send("PASS ".encode())
        clientPassword=client.recv(1024).decode()
        if authenticate_client(clientUsername,clientPassword):
            print("Client authenticated ")
            client.send("Authentication Success".encode())
            clients.append(client)
            usernames.append(clientUsername)
            server.close()

        else:
            print("Client authentication failed")
            client.send("Authentication failed".encode())
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

def receive_files():
    try:
        file_info=server.recv(1024).decode()
        if not file_info:
            return
        file_name,file_size_str=file_info.split(',')
        file_size=int(file_size_str)

        print(f"Receiving {file_name},{file_size} bytes...")

        with open(f"received_{file_name}",'wb') as file:
            bytes_received=0
            while bytes_received<file_size:
                byte_read=server.recv(4096)
                if not byte_read:
                    break
                file.write(byte_read)
                bytes_received+=len(byte_read)
            print(f"{file_name} received Size:{file_size}")
    
    except Exception as e:
        print(f"Error receiving file : {e}")

    receive_thread=threading.Thread(target=receive_files)
    receive_thread.start()


def send_files():
    try:
        file_name=server.recv(1024).decode()
        file_size=os.path.getsize(file_name)
        server.sendall(f"{file_name},{file_size}".encode())

        with open(file_name,"rb") as file:
            while True:
                byte_read=file.read(4096)
                if not byte_read:
                    break
                server.sendall(byte_read)
            print(f"{file_name}:{file_size} sent to the client")

    except FileNotFoundError:
        print(f"{file_name} is not found in the server")

    send_thread=threading.Thread(target=send_files)
    send_thread.start()