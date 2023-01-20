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
    def setUser(self,name,password):
        self.user.setName(name)
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
            data=json.loads(recv)
            return data['result']
        else:
            self.close()
            print("close")

    def sendMsg(self):
        data=json.dumps(self.msg)
        self.tcp.send(data.encode())

    def close(self):
        self.tcp.close()

class UPDClient:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def recvMsg(self):
        return self.udp.recv(1024)

    def sendMsg(self,msg):
        self.udp.sendTo(msg,(self.host,self.port))


if __name__=="__main__":
    temp=TCPClient("127.0.0.1",8080)
    temp.connect()
    temp.setUser("ts","18772463791")
    temp.setMsg("register")
    temp.sendMsg()
    print(temp.recvMsg())
    temp.close()
