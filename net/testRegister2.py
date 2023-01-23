from client import TCPClient
from client import UDPClient
tcp=TCPClient("127.0.0.1",8080)
tcp.setUser("admin")
tcp.setPassword("18772463791")
tcp.setMsg("register")
tcp.sendMsg()
msg=tcp.recvMsg()
if msg["result"]:
    print("successfully register")
else:
    print("fail to register")
#udp=UDPClient("127.0.0.1",8080)
#udp.setUser("ts")
#udp.setFriend("admin")
#udp.setMsg("hello world")
#udp.sendMsg()
    


