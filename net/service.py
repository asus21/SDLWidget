import socket
from database import Database
import json
import re
import time
from threading import Thread,Lock
from queue import Queue
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

    def recvMsg(self):
        recv=self.conn.recv(1024).decode()
        if recv:
            user,friend,msg=recv.split("_")

class TCPService:
    def __init__(self,addr,port):
        self.addr=addr
        self.port=port
        self.tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp.bind((addr,port))
        self.tcp.listen(5)
        self.isRun=True
        self.db=Database("dbChat.db")
        self.db.create_usersTable()
        self.queue=Queue()

    def main(self):
        Thread(target=self.connect).start()
        while self.isRun:
            msg={"item":None,'result':None}
            if not self.queue.empty():
                data=self.queue.get()
                if data['item']=='register':
                    msg["item"]='register'
                    msg["result"]=True
                    self.db.add_userData([data["user"],data['password']])
                elif data['item']=='verify':
                    msg["item"]='verify'
                    msg["result"]=True
                    if not self.db.is_existsUser(data['user']):
                        msg['result']=False
                elif data['item']=='modify':
                    msg["item"]='modify'
                    msg["result"]=True
                    self.db.update_userPassword(data['user'],data['password'])
                self.sendMsg(data['connect'],json.dumps(msg).encode())

    def connect(self):
        while self.isRun:           
            conn,addr=self.tcp.accept()          
            print("\r>> link to address:",addr,end="\n>> ")
            td=Thread(target=self.recvMsg,args=(conn,))
            td.start()

    def sendMsg(self,conn,msg):                     
        conn.send(msg)
        conn.close()
        
    def recvMsg(self,conn):  
        recv=conn.recv(1024)
        if(recv):
            data=json.loads(recv)
            data["connect"]=conn 
            self.queue.put(data)
        else:
            conn.close()
            print("exits",end="\n>> ")


class UDPService:
    def __init(self,addr,port): 
        self.addr=addr
        self.port=port
        self.udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp.bind((addr,portp))
        self.isRun=True

    def connect(self):
        
if __name__=="__main__":
    temp=TCPService("127.0.0.1",8080)
    temp.main()
