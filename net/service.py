import socket
from database import Database
class Service:
    def __init__(self,addr,port):
        self.addr=addr
        self.port=port
        self.db=Database("dbChat.db")
        self.service=socket.socket()
        self.service.bind((addr,port))
        self.service.listen(5)
    def connect(client,address):
        self.conn,self.addr=self.service.accept()
    def recvMsg(self)
        recv=self.conn.recv(1024).decode()
        if recv:
            user,friend,msg=recv.split("_")
