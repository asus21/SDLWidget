import socket
from threading import Thread
from user import User
import json
class Client:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.client=socket.socket()

    def connect(self);
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
        self.msg={"item":None,"user":None,"passord":None,"friend":None} 
    def setUser(self,name,password):
        self.user.setName(name)
        self.user.setPassword(password) 

    def addFriend(self,friendName):
        self.user.addFriend(friendName)
    
    def setMsg(self,item):
        self.msg['item']=item
        self.msg['user']=self.user.getName()
        self.msg['password']=self.user.getPassword()
        self.msg['friend']=self.user.friend()

    def connect(self):
        self.tcp.connect((self.host,self.port))

    def recvMsg(conn):                     
        recv=conn.recv(1024)
        if recv:
            data=json.loads(recv)
            return data['result']
        else:
            conn.close()
            print("close")

    def sendMsg(conn):
        data=json.dumps(self.msg)
        conn.send(data.encode())

    def close(self):
        self.tcp.close()

if __name__=="__main__":
    temp=TCPClient("127.0.0.1",8080)
    temp.connect()
    temp.setUser("ts","18772463791")
    temp.setMsg("register")
    temp.sendMsg()
    print(emp.recvMsg())
