import socket
from threading import Thread
from net.user import User
import json
class TCPClient:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.tcp=socket.socket()
        self.msg={"item":None,"user":None,"password":None} 
        self.tcp.connect((self.host,self.port))

    def setUser(self,name):
        self.msg['user']=name

    def setPassword(self,password):
        self.msg['password']=password

    def setMsg(self,item):
        '''
        item:verify(验证登录),register(注册账号),modify(修改密码)
        '''
        self.msg['item']=item

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
        self.msg={"item":None,"user":None,"friend":None,"msg":None}

    def recvMsg(self):
        recv=self.udp.recv(1024)
        if recv:
            data=json.loads(recv)
            return data['msg']
    
    def addFriend(self,friendName):
        self.msg['friend']=friendName

    def setUser(self,name):
        self.msg["user"]=name
        self.msg["item"]="Ip"
        self.sendMsg()

    def setFriend(self,friend):
        self.msg["friend"]=friend

    def setItem(self,item):
        '''
        item:Ip(发送Ip),addfriend(添加朋友),deletefriend(删除好友),exit(退出登录),send(发送消息)
        '''
        self.msg["item"]=item

    def setMsg(self,msg):
        self.msg['item']="send"
        self.msg["msg"]=msg

    def sendMsg(self):
        self.udp.sendto(json.dumps(self.msg).encode(),(self.host,self.port))

    def close(self):
        self.msg["item"]="exit"
        self.sendMsg()
        self.udp.close()

if __name__=="__main__":
    temp=TCPClient("127.0.0.1",8081)
    temp.setUser("ts")
    temp.setMsg("register")
    temp.sendMsg()
    print(temp.recvMsg())
    temp.close()
