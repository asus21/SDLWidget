import socket
import sys
import re
from threading import Thread
class Service:
    def __init__(self,addr,port):
        self.addr=addr
        self.port=port
        self.sevice=socket.socket()
    
def connectShow(client):
    txt='''
    what do you want to do?\n
    1. chat with friend\n
    2. contact custoner service
    '''.encode()
    client.send(txt)
def choiceExecute(client):
    txt="please input your friend's ip".encode()
    client.send(txt);

def prompt():
    print(">> ",end="")


def showlist(addr):
    print("client online:")
    for i in range(len(addr)):
        print(i+1,"\t",addr[i][0],":",addr[i][1])


def chat(conn,addr):
    global isrun
    while isrun:
        global address,client
        index=address.index(addr)
        recv=conn.recv(1024).decode()
        if(recv):
            if(recv !="quit/" and recv!="exit/"):
                print(address[index][1],":",recv,end="\n>> ")
            if(recv=="1"):
                choiceExecute(conn) 
            else:
                conn.close()
                print(address[index][0],":",address[index][1],"exits",end="\n>> ")
                client.pop(index)
                address.pop(index)
                break
        else:
            conn.close()
            print(address[index][0],":",address[index][1],"exits",end="\n>> ")
            address.pop(index) 
            client.pop(index)   
            break


def serviceIn():
    global isrun
    while isrun:
        global client
        temp=input().split(" ")
        text=" ".join(temp[1:])
        try:
            if(temp[0]=="exit/" or temp[0]=="quit/"):
                isrun=False
                break
            elif(len(client)==0):
                print("no client linking",end="\n>> ")
                continue
            elif(temp[0]=="help/"):
                print("")
            elif(temp[0]=="list/"):
                td=Thread(target=showlist,args=(address,))
                td.start()
                td.join()
                prompt()
                continue
            elif(temp[0]=="kick/"):
                client[int(text)-1].send("kick/".encode())
                continue
            elif(temp[0]==""):
                prompt()
                continue
            if(not re.findall(r"[0-9]+",temp[0])):
                for i in client:
                    i.send(" ".join(temp[0:]).encode())
                    prompt()
            else:
                index=int(temp[0])-1
                client[index].send(text.encode())
                prompt()
        except:
            prompt()
        

def moniter(client,address):
    global isrun
    flag=True
    while isrun:
        conn,addr=web.accept()
        client.append(conn)
        address.append(addr)
        print("\r>> link to address:",addr,end="\n>> ")
        td=Thread(target=chat,args=(conn,addr))
        td.start()
        if(flag):
            Thread(target=serviceIn,daemon=True).start()
            flag=False

isrun=True
host=sys.argv[1]
port=int(sys.argv[2])
web=socket.socket()
web.bind((host,port))
web.listen(5)
client=[]
address=[]
prompt()
print("start listening")
Thread(target=moniter,args=(client,address),daemon=True).start()
while isrun:
    pass

for i in client:
    i.send("close/".encode())
web.close()
sys.exit(0)
