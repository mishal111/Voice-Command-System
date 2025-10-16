import socket
import getpass
import threading
import os

host='127.0.0.1'
port = 55555
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

def client_handle():
    while True:
        message=client.recv(1024).decode()
        if not message:
            print("Connection Error")
            return
        if message.startswith("UN"):
            username=getpass.getpass("> Enter your username: ")
            client.sendall(username.encode())
        elif message.startswith("PASS"):
            password=getpass.getpass("> Enter your password: ")
            client.sendall(password.encode())
        elif message.startswith("AUTH SUCCESS"):
            print("Authentication Success")
            threading.Thread(target=client_handle_server , daemon=True).start()
            
        else:
            print (message)

def client_handle_server():
    while True:
        client_command=input(">> ").strip()
        if not client_command:
            continue
        try:
            if client_command == "LIST":
                client.sendall("LIST".encode())

            elif client_command == "SEND":
                upload_server()

            elif client_command == "DOWNLOAD":
                download_server()

            elif client_command == "HELP":
                print("----HELP----\nLIST : List all files \n UPLOAD : Upload a file to the server \n DOWNLOAD : Download a file from the server \n HELP : List all available commands")

            else:
                print("Unknown Command. Try HELP for for commands")
        except:
            print("Could not read command")
        
    
def upload_server():
    try:
        client.send("UPLOAD".encode())

        filepath=input("Enter file's filepath: ")
        fileName=filepath.rsplit('/',1)[-1]
        fileSize=os.path.getsize(filepath)
        client.sendall(f"{fileName},{fileSize}")

        if client.recv(1024).decode().startswith("META_DATA_ACK"):
            try:
                with open(filepath,'rb') as file:
                    while True:
                        byte_read=file.read(4096)
                        if not byte_read:
                            break
                        client.sendall(byte_read)
                    print(f"{fileName}:{fileSize} is uploaded")
        
            except FileNotFoundError:
                print(f"{fileName} is not found")
    
    except Exception as e:
        print(f"Upload Failed: {e}")

def download_server():
    try:
        fileInfo=client.recv(1024).decode()
        if not fileInfo:
            return
        elif fileInfo:
            client.send("META_DATA_ACK".encode())

        fileName,fileSizeStr=fileInfo.split(',',1)
        fileSize=int(fileSizeStr)

        with open(f"received_{fileName}",'wb') as file:
            byte_received=0
            while byte_received<fileSize:
                byte_read=client.recv(4096)
                if not byte_read:
                    break
                file.write(byte_read)
                byte_received +=len(byte_read)
        print(f"{fileName} Downloaded {fileSize}bytes")
    
    except Exception as e:
        print(f"Error receiving file:{e}")

threading.Thread(target=client_handle,daemon=True).start()

while True:
    pass