import socket
import Users
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
