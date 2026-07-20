import threading
import socket

def recvmsg(con):
    while True:
        message=con.recv(1024).decode()
        if not message:
            break
        print("message by User -> :",message)




Addr=("127.0.0.1",5050)
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(Addr)
server.listen(1)
con,addr=server.accept()
threading.Thread(target=recvmsg,args=(con,),daemon=True).start()

while True:
    message=input("Type Message : ->")
    con.send(message.encode())
    if message.lower()=="exit":
        break

con.close()
server.close()