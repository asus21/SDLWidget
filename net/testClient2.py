from client import TCPClient
from client import UDPClient

tcp=TCPClient("127.0.0.1",8080)
tcp.setUser("admin")
tcp.setPassword("18772463791")
tcp.setMsg("verify")
tcp.sendMsg()
msg=tcp.recvMsg()
udp=UDPClient("127.0.0.1",8081)
print(msg)
tcp.close()
if msg["result"]:
    udp.setUser("admin")
    data=udp.recvMsg()
    print(data)
    udp.setMsg("Thanks for your feedback")
    udp.sendMsg()
else:
    udp.close()
    print("not register")
    


