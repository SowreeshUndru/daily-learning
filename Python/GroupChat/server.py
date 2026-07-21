import threading
import socket



def recvmsg(cl):
    while True:
        message=cl.recv(1024).decode()
        if not message:
            clients.remove(cl)
            cl.close()
            break 
        if message.lower()=="exit":
            clients.remove(cl)
            cl.close()
            break
        for client in clients:
            if cl==client:
                continue
            else:
                client.send(message.encode())

            

server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("127.0.0.1",5050))
server.listen()
clients=[]
while True:
    client,addr=server.accept()
    clients.append(client)
    threading.Thread(target=recvmsg,args=(client,),daemon=True).start()