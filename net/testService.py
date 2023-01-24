from service import TCPService
from service import UDPService
from multiprocessing import Process
from threading import Thread
tcp=TCPService("127.0.0.1",8080)
udp=UDPService("127.0.0.1",8081)
try:
    Thread(target=tcp.main).start()
    Thread(target=udp.main).start()
except:
    tcp.close()
    udp.close()
