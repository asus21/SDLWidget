import socket
from database import Database
import json
import re
from threading import Thread
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
        self.client=[]
        self.address=[]
        self.isRun=True
        self.db=Database("dbChat.db")

    def main(self):
        Thread(target=self.connect,daemon=True).start()

    def connect(self):
        while self.isRun:           
            conn,addr=self.tcp.accept()          
#            self.client.append(conn)
#            self.address.append(addr)
            print("\r>> link to address:",addr,end="\n>> ")
            td=Thread(target=self.recvMsg,args=(conn,addr))
            td.start()

    def sendMsg(self,conn,msg):                     
        conn.send(msg)
        conn.close()
        
    def recvMsg(self,conn,addr):  
        recv=conn.recv(1024)
        if(recv):
            msg={"type":None,'result':None}
            data=json.loads(recv)
            if data['type']=='register':
                 msg["type"]='register'
                    msg["result"]=True

                    self.db.add_userData([data["user"],data['password']])
                    self.sendMsg(conn,json.dumps(msg).encode())
                    break
                elif data['type']=='verify':
                    msg["type"]='verify'
                    msg["result"]=True
                    if not self.db.is_existsUser(data['user']):
                        msg['result']=False
                    self.sendMsg(conn,json.dumps(msg).encode())
                    break
                elif data['type']=='modify':
                    msg["type"]='modify'
                    msg["result"]=True
                    self.db.update_userPassword(data['user'],data['password'])
                    self.sendMsg(conn,json.dumps(msg).encode())
                    break
            else:
                conn.close()
                print(self.address[index][0],":",self.address[index][1],"exits",end="\n>> ")
                self.address.pop(index)
                self.client.pop(index)
                break


class UDPService:
    def __init(self,addr,port): 
        self.addr=addr
        self.port=port
        self.udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
if __name__=="__main__":
    temp=TCPService("127.0.0.1",8081)
    temp.main()
