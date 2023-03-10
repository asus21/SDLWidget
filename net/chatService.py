import signal
import sys
from service import TCPService
from service import UDPService
from threading import Thread
tcp=TCPService("0.0.0.0",8080)
udp=UDPService("0.0.0.0",8081)
def fun(a,b):
    global tcp,udp
    tcp.shutdown()
    udp.shutdown()
    print("ok")
print("start service")
td1=Thread(target=tcp.main)
td2=Thread(target=udp.main)
signal.signal(signal.SIGINT, fun)
td1.start()
td2.start()
td1.join()
td2.join()
