from client import TCPClient
from client import UDPClient

tcp=TCPClient("127.0.0.1",8080)
tcp.setUser("admin")
tcp.setPassword("18772463791")
tcp.setMsg("verify")
tcp.sendMsg()
msg=tcp.recvMsg()
print(msg)
if msg["result"]:
    udp=UDPClient("127.0.0.1",8081)
    while True:
        udp.setUser("admin")
        data=udp.recvMsg()
        print(data)
        udp.setMsg("Thanks for your feedback")
        udp.sendMsg()
else:
    print("not register")
    


