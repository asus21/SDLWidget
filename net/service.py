import socket
from database import Database
import json
import re
import time
from threading import Thread,Lock
from queue import Queue
import sys
sys.path.append('.')
sys.path.append("..")
from utils.alert import alert
from constent import *
#ERROR_NOT_EXITUSER="Dones't exit the user,please register"
#ERROR_NOT_CORRECTPASSWORD="Password isn't correct "
#ERROR_NULL_USER="The username is empty"
#ERROR_NULL_PASSWORD="The password is empty"
#ERROR_DIFFER_PASSWORD="It's different from twice password input"
#ERROR_FAIL_TO_OPERATEDATABASE="Fail to operate database"
#ERROR_CONNECT_QUIT="Service is closed"
class TCPService:
    '''tcp服务器主要用于信息验证'''
    def __init__(self,addr,port):
        self.addr=addr
        self.port=port
        self.tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.tcp.bind((addr,port))
        self.tcp.listen(5)
        self.isRun=True
        self.queue=Queue()

    def main(self):
        '''主函数用于实现服务器功能'''
        self.db=Database("dbChat.db")
        self.db.create_usersTable()
        self.db.add_userData(["admin","admin"])
        Thread(target=self.connect,daemon=True).start()#在子线程中等代客户端连接防止主线程阻塞
        while self.isRun:
            if not self.queue.empty():
                msg={"item":None,'result':None,'error':None}
                data=self.queue.get()
                if data['item']=='register':
                    if self.__checkUser(data,msg) and self.__checkPassword(data,msg) and self.__checkAgain(data,msg):
                        msg["item"]='register'
                        try:              
                            self.db.add_userData([data["user"],data['password']])
                            self.db.add_friendData([data["user"],"admin"])
                            self.db.add_friendData(["admin",data["user"]])
                            msg["result"]=True
                        except:
                            msg["result"]=False
                            msg['error']=ERROR_FAIL_TO_OPERATEDATABASE
                elif data['item']=='verify':
                    msg["item"]='verify'
                    if self.__checkUser(data,msg) and self.__checkPassword(data,msg):
                        if not self.db.is_existsUser(data['user']):
                            msg['result']=False
                            msg['error']=ERROR_NOT_EXITUSER
                        else:
                            try:
                                if self.db.query_userPassword(data["user"])==data['password']:
                                    msg["friends"]=self.db.query_userFriends(data["user"])
                                    msg["result"]=True
                                else:
                                    msg['result']=False
                                    msg["error"]=ERROR_NOT_CORRECTPASSWORD
                            except:
                                msg["result"]=False
                                msg['error']=ERROR_FAIL_TO_OPERATEDATABASE
                elif data['item']=='modify':
                    msg["item"]='modify'
                    if self.__checkUser(data,msg) and self.__checkPassword(data,msg):
                        try:
                            self.db.update_userPassword(data['user'],data['password'])
                            msg["result"]=True
                        except:
                            msg["result"]=False
                            msg["error"]=ERROR_NOT_CORRECTPASSWORD
                elif data['item']=='quit':
                    break
                self.sendMsg(data['connect'],json.dumps(msg).encode())
        self.close()

    def connect(self):
        '''等待链接'''
        while self.isRun:           
            conn,addr=self.tcp.accept()         
            try: 
                assert False,print("\r>> (tcp)link to address:",addr,end="\n>> ")
            except:
                pass
            Thread(target=self.recvMsg,args=(conn,),daemon=True).start()
    def __checkUser(self,data,msg):
        if data["user"]:
            msg['result']=True
            return True
        else:
            msg['result']=False
            msg['error']=ERROR_NULL_USER
            return False
            
    def __checkPassword(self,data,msg):
        if data['password']:
            msg['result']=True
            return True
        else:
            msg['result']=False
            msg['error']=ERROR_NULL_PASSWORD
            return False
    def __checkAgain(self,data,msg):
        if data['password']==data['again']:
            msg['result']=True
            return True
        else:
            msg['result']=False
            msg['error']=ERROR_DIFFER_PASSWORD
            return False
    def sendMsg(self,conn,msg):                     
        '''发送消息'''
        conn.send(msg)
        
    def recvMsg(self,conn):  
        '''接受消息'''
        while self.isRun:
            recv=conn.recv(1024)
            if(recv):
                data=json.loads(recv)
                alert(data)
                data["connect"]=conn 
                self.queue.put(data)
                alert(data)
            else:
                conn.close()
                try:
                    assert False,print("(tcp)exits",end="\n>> ")
                except:
                    pass
                break
    def shutdown(self):
        self.queue.put({"item":"quit"})
    def close(self):
        '''关闭服务端'''
        while not self.queue.empty():
            msg={"item":quit,'result':False,'error':ERROR_CONNECT_QUIT}
            data=self.queue.get()
            self.sendMsg(data['connect'],json.dumps(msg).encode())
            data['connect'].close()
        self.tcp.close()
        self.db.close()
        self.isRun=False
        print("all exit")

class UDPService:
    '''udp服务器主要用于信息发送'''
    def __init__(self,addr,port): 
        self.addr=addr
        self.port=port
        self.udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp.bind((addr,port))
        self.isRun=True
        self.queue=Queue()

    def main(self):
        self.db=Database("dbChat.db")
        self.db.create_usersLogTable()
        self.db.create_friendsTable()
        Thread(target=self.recvMsg,daemon=True).start()
        while self.isRun:
            if not self.queue.empty():
                msg={"sendUser":None,'msg':None}
                data=self.queue.get()
                if data['item']=="exit":
                    self.db.delete_userLogData(data["user"])
                    alert("(udp)exits")
                elif data["item"]=="send":
                    msg["sendUser"]=data["user"]
                    msg["msg"]=data["msg"]
                    if self.db.is_existsUserLog(data["friend"]):
                        _,ip,port=self.db.query_usersLog(data["friend"])
                        try: 
                            assert False,print("sendto:",(ip,port)," msg:",msg)
                        except:
                            pass
                        self.sendMsg(msg,(ip,port))
                    else:
                        self.queue.put(data)
                elif data["item"]=="Ip":
                    self.db.add_userLog([data["user"],data["address"][0],data["address"][1]])
                elif data["item"]=="addfriend":
                    self.db.add_friendData([data["user"],data["friend"]])
                elif data["item"]=="deletefriend":
                    self.db.delete_friendData(data["user"])
                elif data["item"]=="quit":
                    break
        self.close()

    def recvMsg(self):
        '''接受消息'''
        while self.isRun:
            recv,addr=self.udp.recvfrom(1024)
            try:
               assert False,print("\r>> (udp)link to address:",addr,end="\n>> ")
            except:
                pass
            if recv:
                data=json.loads(recv)
                alert(data)
                data["address"]=addr 
                self.queue.put(data)
            
    def sendMsg(self,msg,addr):
        '''发送消息'''
        self.udp.sendto(json.dumps(msg).encode(),addr)

    def shutdown(self):
        self.queue.put({'item':'quit'})
    def close(self):
        '''关闭服务端'''
        self.udp.close()
        self.db.delete_userLogDatas()#删除所有在线用户
        self.db.close()

if __name__=="__main__":
    temp=TCPService("127.0.0.1",8081)
    temp.main()
