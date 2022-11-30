import socket
import sys
from threading import Thread

def prompt():
    print(">> ",end="")

def connectShow(client):
    txt='''
    what do you want to do?\n
    1. chat with friend\n
    2. contact custoner service
    '''.encode()
    client.send(txt)

def recvMsg(conn):
    global isrun
    while isrun:
        recv=conn.recv(1024).decode() 
        if(recv=="kick/"):
            print("you have been kicked off")
            conn.close()
            isrun=False
            break
        elif(recv=="close/"):
            print("the remote service has closed the link")
            conn.close()
            isrun=False
            break
        elif(recv):
            print(" response:",recv,end="\n>> ")

def sendMsg(conn):
    global isrun
    while isrun:
        text=input(">> ")
        if(text=="quit/" or text=="exit/"):
            isrun=False
            break 
        conn.send(text.encode())



isrun=True
host=sys.argv[1]
port=int(sys.argv[2])
conn=socket.socket()
try:
    conn.connect((host,port))
except:
    print("the remote service has closed the link ")
    sys.exit(0)
print("****************************************************************")
print("*         exit: enter  'quit/' or 'exit/'                      *")
print("*         send: enter message both English and Chinese support *")
print("*                                                              *")
print("****************************************************************")
prompt()
print("successfully connect")
Thread(target=recvMsg,args=(conn,),daemon=True).start()
Thread(target=sendMsg,args=(conn,),daemon=True).start()
while isrun:
    pass

sys.exit(1)
