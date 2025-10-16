import socket
import threading
import os
import getpass

host ='127.0.0.1'
port = 55555
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
    
print(f"Server is listening on {host}:{port}...")

def authenticate_client(clientUsername,clientPassword):
    with open(os.path.expanduser('~/Documents/pass.txt'),'r') as file:
        for line in file:
            line=line.strip()
            if '=' in line:
                username,password = line.split('=',1)
                username=username.strip()
                password=password.strip()
                if clientUsername==username and clientPassword==password:
                    return True
            
    return False


def client_handle():

    while True:
        client,address=server.accept()

        client.send("UN".encode())
        clientUsername=client.recv(1024).decode()
        client.send("PASS ".encode())
        clientPassword=client.recv(1024).decode()

        if authenticate_client(clientUsername,clientPassword):
            print("Client authenticated ")
            client.send("AUTH SUCCESS".encode())
            clients.append(client)
            usernames.append(clientUsername)

        else:
            print("Client authentication failed")
            client.send("Authentication failed".encode())
            client.close()
            break
        client_command = client.recv(1024).decode()
        if client_command == "LIST":
            files=os.listdir()
            client.sendall("\n".join(files).encode())

        elif client_command == "DOWNLOAD":
            upload_files()

        elif client_command == "UPLOAD":
            download_files()
        
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
            elif server_input=="EXIT":
                print("Shutting Down Server")
                for client in clients:
                    try:
                        client.sendall("SERVER_SHUTDOWN".encode())
                        client.close()
                    except:
                        pass
                server.close()
                os._exit(0)
            elif server_input == 'DELETE':
                rmFile=input("> Name of the file >> ")
                try:
                    os.remove(rmFile)
                    print(f"{rmFile} is removed")

                except FileNotFoundError:
                    print(f"Error: {rmFile} does not exist")

    else:
        print("Authentication failed")
    
def download_files():
    for client in clients:
        try:
            file_info=client.recv(1024).decode()
            if not file_info:
                return
            elif file_info:
                client.sendall("META_DATA_ACK".encode())

            file_name,file_size_str=file_info.split(',')
            file_size=int(file_size_str)

            print(f"Receiving {file_name},{file_size} bytes...")

            with open(f"received_{file_name}",'wb') as file:
                bytes_received=0
                while bytes_received<file_size:
                    byte_read=client.recv(4096)
                    if not byte_read:
                        break
                    file.write(byte_read)
                    bytes_received+=len(byte_read)
                print(f"{file_name} received Size:{file_size}")
        
        except Exception as e:
            print(f"Error receiving file : {e}")

def upload_files():
    for client in clients:
        try:
            file_name=client.recv(1024).decode()
            file_size=os.path.getsize(file_name)
            client.sendall(f"{file_name},{file_size}".encode())

            if client.recv(1024).decode().startswith("META_DATA_ACK"):
                try:

                    with open(file_name,"rb") as file:
                        while True:
                            byte_read=file.read(4096)
                            if not byte_read:
                                break
                            client.sendall(byte_read)
                        print(f"{file_name}:{file_size} sent to the client")

                except FileNotFoundError:
                    print(f"{file_name} is not found in the server")

        except Exception as e:
            print(f"Upload Failed: {e}")

threading.Thread(target=server_handle, daemon=True).start()
threading.Thread(target=client_handle).start()