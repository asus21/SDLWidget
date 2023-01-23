from service import TCPService
from service import UDPService
from multiprocessing import Process
tcp=TCPService("127.0.0.1",8080)
udp=UDPService("127.0.0.1",8081)
try:
    Process(target=tcp.main).start()
    Process(target=udp.main).start()
except:
    tcp.close()
    udp.close()
