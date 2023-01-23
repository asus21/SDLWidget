import socket
from threading import Thread
from user import User
import json
class Client:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.client=socket.socket()

    def connect(self):
        try:
            self.client.connect((self.host,self.port))
            return 1
        except:
            return -1

    def sendMsg(self,user,friend,msg):
        '''
        user:the name of user
        friend:the name of user's friend
        msg:a messges the user wants to send
        
        '''
        self.client.send((user+"_"+friend+"_"+msg).encode())

    def recvMsg(conn):
        recv=self.client.recv(1024).decode()
        return recv

class TCPClient:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.tcp=socket.socket()
        self.user=User()
        self.msg={"item":None,"user":None,"password":None,"friend":None} 
        self.connect()
    def setUser(self,name):
        self.user.setName(name)

    def setPassword(self,password):
        self.user.setPassword(password) 

    def addFriend(self,friendName):
        self.user.addFriend(friendName)
    
    def setMsg(self,item):
        self.msg['item']=item
        self.msg['user']=self.user.getName()
        self.msg['password']=self.user.getPassword()
        self.msg['friend']=self.user.getFriends()

    def connect(self):
        self.tcp.connect((self.host,self.port))

    def recvMsg(self):                     
        recv=self.tcp.recv(1024)
        if recv:
            return json.loads(recv)
        else:
            self.close()
            print("close")

    def sendMsg(self):
        data=json.dumps(self.msg)
        self.tcp.send(data.encode())

    def close(self):
        self.tcp.close()

class UDPClient:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.msg={"user":None,"friend":None,"msg":None}

    def recvMsg(self):
        recv=self.udp.recv(1024)
        if recv:
            data=json.loads(recv)
            return data['msg']
    
    def setUser(self,name):
        self.msg["user"]=name
        self.sendMsg()

    def setFriend(self,friend):
        self.msg["friend"]=friend

    def setMsg(self,msg):
        self.msg["msg"]=msg

    def sendMsg(self):
        self.udp.sendto(json.dumps(self.msg).encode(),(self.host,self.port))

if __name__=="__main__":
    temp=TCPClient("127.0.0.1",8081)
    temp.setUser("ts")
    temp.setMsg("register")
    temp.sendMsg()
    print(temp.recvMsg())
    temp.close()
