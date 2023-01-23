from client import TCPClient
from client import UDPClient
tcp=TCPClient("127.0.0.1",8080)
tcp.setUser("ts")
tcp.setPassword("18772463791")
tcp.setMsg("verify")
tcp.sendMsg()
msg=tcp.recvMsg()
print(msg)
if msg["result"]:
    udp=UDPClient("127.0.0.1",8081)
    while True:
        udp.setUser("ts")
        udp.setFriend("admin")
        udp.setMsg("hello world")
        udp.sendMsg()
        data=udp.recvMsg()
        print(data)
else:
    print("not register")
#udp=UDPClient("127.0.0.1",8080)
#udp.setUser("ts")
#udp.setFriend("admin")
#udp.setMsg("hello world")
#udp.sendMsg()
    


