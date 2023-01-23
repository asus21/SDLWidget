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
        self.db.create_usersLogTable()
        self.db.create_friendsTable()
        self.queue=Queue()

    def main(self):
        Thread(target=self.connect).start()
        while self.isRun:
            if not self.queue.empty():
                msg={"item":None,'result':None}
                data=self.queue.get()
                if data['item']=="exit":
                    msg["item"]="exit"
                    msg["result"]=True
                    self.sendMsg(data['connect'],json.dumps(msg).encode())
                    self.db.delete_userLogData(data["user"])
                else:
                    if data['item']=='register':
                        msg["item"]='register'
                        msg["result"]=True
                        self.db.add_userData([data["user"],data['password']])
                    elif data['item']=='verify':
                        msg["item"]='verify'
                        if not self.db.is_existsUser(data['user']):
                            msg['result']=False
                        else:
                            msg["result"]=True
                            msg["friends"]=self.db.query_userFriends(data["user"])
                            self.db.add_userLog([data["user"],data["connect"].getsockname()[0],None])
                    elif data['item']=='modify':
                        msg["item"]='modify'
                        msg["result"]=True
                        self.db.update_userPassword(data['user'],data['password'])
                    self.sendMsg(data['connect'],json.dumps(msg).encode())

    def connect(self):
        while self.isRun:           
            conn,addr=self.tcp.accept()         
            print("\r>> (tcp)link to address:",addr,end="\n>> ")
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

    def close(self):
        self.tcp.close()
        self.db.close()

class UDPService:
    def __init__(self,addr,port): 
        self.addr=addr
        self.port=port
        self.udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp.bind((addr,port))
        self.isRun=True
        self.queue=Queue()
        self.db=Database("dbChat.db")
        self.db.create_usersTable()
        self.db.create_usersLogTable()
        self.db.create_friendsTable()

    def main(self):
        Thread(target=self.recvMsg).start()
        while self.isRun:
            if not self.queue.empty():
                msg={"sendUser":None,'msg':None}
                data=self.queue.get()
                if data["msg"]:
                    msg["sendUser"]=data["user"]
                    msg["msg"]=data["msg"]
                    if self.db.is_existsUserLog(data["friend"]):
                        _,ip,port=self.db.query_usersLog(data["friend"])
                        print("sendto:",(ip,port))
                        self.sendMsg(msg,(ip,port))
                    else:
#                        print("the user you want to send msg isn't online")
                        self.queue.put(data)
                else:
                    print("update",data["address"])
                    self.db.update_usersPort(data["user"],data["address"][1])

    def recvMsg(self):
        while self.isRun:
            recv,addr=self.udp.recvfrom(1024)
            print("\r>> (udp)link to address:",addr,end="\n>> ")
            if recv:
                data=json.loads(recv)
                data["address"]=addr 
                self.queue.put(data)
            
    def sendMsg(self,msg,addr):
        self.udp.sendto(json.dumps(msg).encode(),addr)

    def close(self):
        self.udp.close()
        self.db.close()

if __name__=="__main__":
    temp=TCPService("127.0.0.1",8081)
    temp.main()
