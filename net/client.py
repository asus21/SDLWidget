import socket
from threading import Thread
import json
from net.constent import *
class Client:
    def __init__(self,config='config.json'):
        with open(config) as f:
            date=json.load(f)
        host=data["remote_ip"]
        port_tcp=data['port_tcp']
        port_udp=data['port_udp']

    def setUser(self,data):
        self.tcp=TCPClient(host,port_tcp)


class TCPClient:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.tcp=socket.socket()
        self.data={"item":None,"user":None,"password":None} 
        self.tcp.connect((self.host,self.port))

    def setData(self,data)->None:
        '''
        item:verify(验证登录),register(注册账号),modify(修改密码)
        '''
        self.data=data
        
    def recvMsg(self)->dict:               
        '''返回接受消息'''
        recv=self.tcp.recv(1024)
        if recv:
            return json.loads(recv)
        else:
            self.close()
            return {"item":"quit","result":False,"error":ERROR_CONNECT_QUIT} 

    def sendMsg(self):
        self.tcp.send(json.dumps(self.data).encode())

    def close(self):
        self.tcp.close()

class UDPClient:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.msg={"item":None,"user":None,"friend":None,"msg":None}

    def recvMsg(self)->str:
        '''返回接受消息
        return data={"sendUser":None,"msg":None}
        '''
        recv=self.udp.recv(1024)

        if recv:
            data=json.loads(recv)
            return data
    
    def addFriend(self,friendName)->str:
        self.msg['friend']=friendName

    def setUser(self,name)->None:
        self.msg["user"]=name
        self.msg["item"]="Ip"
        self.sendMsg()

    def setFriend(self,friend)->list:
        self.msg["friend"]=friend

    def setItem(self,item)->None:
        '''
        item:Ip(发送Ip),addfriend(添加朋友),deletefriend(删除好友),exit(退出登录),send(发送消息)
        '''
        self.msg["item"]=item

    def setMsg(self,msg)->None:
        self.msg['item']="send"
        self.msg["msg"]=msg

    def sendMsg(self)->None:
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
