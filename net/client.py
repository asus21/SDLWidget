import socket
from threading import Thread
import json
from queue import Queue
from net.constent import *
import sys
sys.path.append("..")
import os
from database.dblocal import dbLocal
class Client:
    def __init__(self,config='config.json'):
        with open(config) as f:#导入配置文件
            data=json.load(f)
        self.host=data["server_ip"]
        self.port_tcp=data['port_tcp']
        self.port_udp=data['port_udp']
        self.udp=None
        self.queue=Queue()

    def setData(self,data):
        '''设置用户信息'''
        self.data=data 

    def create_usr(self):
        if not os.path.exists("/data/data/com.termux/files/home/myChat/usr/"+self.data["user"]):
            os.mkdir("/data/data/com.termux/files/home/myChat/usr/"+self.data["user"])
        os.chdir("/data/data/com.termux/files/home/myChat/usr/"+self.data["user"])
        self.db=dbLocal("dblocal.db")
        self.db.create_msgTable()

    def __error(func):
        def wrapper(self):
            try:
                return func(self)
            except Exception as e:
#                raise e
                return {"result":False,"error":ERROR_NETWORK_FAIL}
        return wrapper

    @__error
    def verify(self):
        '''登录'''
        data={"item":"verify"}
        data.update(self.data)
        tcp=TCPClient(self.host,self.port_tcp)
        tcp.send(data)
        msg=tcp.recvMsg()
        tcp.close()
        if msg['result']:
            self.create_usr()
            self.udp=UDPClient(self.host,self.port_udp)
            self.udp.setUser(data["user"])
            Thread(target=self.__handleMsg).start()
        return msg

    @__error
    def register(self):
        '''注册'''
        data={"item":"register"}
        data.update(self.data)
        tcp=TCPClient(self.host,self.port_tcp)
        tcp.send(data)
        msg=tcp.recvMsg()
        tcp.close()
        return msg
    
    @__error
    def modify(self):
        '''修改密码'''
        data={"item":"modify"}
        data.update(self.data)
        tcp=TCPClient(self.host,self.port_tcp)
        tcp.send(data)
        msg=tcp.recvMsg()
        tcp.close()
        return msg

    def __handleMsg(self):
        '''运行在子线程中将发送和接受的消息写入数据库'''
        db=dbLocal("dblocal.db")
        db.create_msgTable()
        Thread(target=self.recvMsg,daemon=True).start()
        while True:
            if not self.queue.empty():
                cmd=self.queue.get()
                if cmd=="close":
                    break
                else:
                    db.add_msgData(cmd)

    def sendMsg(self,friend,msg):
        '''发送消息'''
        data={"item":"send","user":self.data['user'],"friend":friend,"msg":msg}
        self.queue.put([friend,1,msg])
        self.udp.send(data)
    
    def getSendMsg(self,friend=None):
        if friend:
            return self.db.query_friend_send_msg(friend)
        else:
            return self.db.query_all_send_msg()
    
    def getRecvMsg(self,friend=None):
        if friend:
            return self.db.query_friend_recv_msg(friend)
        else:
            return self.db.query_all_recv_msg()

    def getAllMsg(self,friend=None):
        if friend:
            return self.db.query_friend_msg(friend)
        else:
            return self.db.query_all_msg()
            
    def recvMsg(self):
        '''接受消息'''
        while True:
            recv=self.udp.recvMsg()
            self.queue.put([recv["sendUser"],0,recv["msg"]])

    def close(self):
        '''退出登录'''
        self.queue.put("close")
        if self.udp:
            self.udp.close()

     
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

    def send(self,data):
        self.tcp.send(json.dumps(data).encode())

    def close(self):
        self.tcp.close()

class UDPClient:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.msg={"item":None,"user":None,"friend":None,"msg":None}

    def recvMsg(self):
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

    def send(self,msg):
        self.udp.sendto(json.dumps(msg).encode(),(self.host,self.port))

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
