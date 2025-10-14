import socket
import getpass
import threading
import os

host='127.0.0.1'
port = 55557
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))

def command_input():
    while True:
        command=input("> ")
        return command
    
def client_handle():
    while True:
        message=client.recv(1024).decode()
        if not message:
            print("Connection Error")
            return
        if message=="UN":
            username=getpass.getpass("> Enter your username: ")
            client.sendall(username.encode())
        if message=="PASS":
            password=getpass.getpass("> Enter your password: ")
            client.sendall(password.encode())
        else:
            print (message)

def client_handle_server(client_command):
    try:
        if client_command == "LIST":
            client.sendall("LIST".encode())
        elif client_command == "SEND":
            upload_server()
        elif client_command == "DOWNLOAD":
            download_server()
        elif client_command == "HELP":
            print("----HELP----\nLIST : List all files \n UPLOAD : Upload a file to the server \n DOWNLOAD : Download a file from the server \n HELP : List all available commands")

    except:
        print("Could not read command")
        return
    
def upload_server():
    try:
        client.send("DOWNLOAD".encode())
        client.send("UPLOAD".encode())
        filepath=input("Enter file's filepath: ")
        fileName=filepath.rsplit('/',1)[-1]
        fileSize=os.path.getsize(filepath)
        client.sendall(f"{fileName},{fileSize}")

        with open(filepath,'rb') as file:
            while True:
                byte_read=file.read(4096)
                if not byte_read:
                    break
                client.sendall(byte_read)
            print(f"{fileName}:{fileSize} is uploaded")
    
    except FileNotFoundError:
        print(f"{fileName} is not found")

def download_server():
    try:
        fileInfo=client.recv(1024).decode()
        fileName,fileSizeStr=fileInfo.split(',',1)
        fileSize=int(fileSizeStr)

        with open(f"received_{fileName}",'wb') as file:
            byte_received=0
            while byte_received<fileSize:
                byte_read=client.recv(4096)
                if not byte_read:
                    break
                file.write=byte_read
                byte_received +=len(byte_read)
        print(f"{fileName} Downloaded {fileSize}bytes")
    
    except Exception as e:
        print(f"Error receiving file:{e}")