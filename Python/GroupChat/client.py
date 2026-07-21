import threading
import socket

def recvmsg(client):
    while True :
        message=client.recv(1024).decode()
        if not message:
            break
        else :
            print("UserSent:",message)
    client.close()
    




client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",5050))
threading.Thread(target=recvmsg,args=(client,),daemon=True).start()
while True:
    message=input("write the message:")
    if message.lower()=="exit":
        break
    client.send(message.encode())

client.close()