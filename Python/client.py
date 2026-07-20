import threading;
import socket;

def recvmsg(con):
    while True:
        message=con.recv(1024).decode()
        if not message:
            break
        print("user message -> :",message)


server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.connect(("127.0.0.1",5050))

threading.Thread(target=recvmsg,args=(server,),daemon=True).start()

while True:
    message=input("message to send")
    if message.lower()=="exit":
        break
    server.send(message.encode())

server.close()