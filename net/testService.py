from service import TCPService
from service import UDPService
from multiprocessing import Process
from threading import Thread
tcp=TCPService("127.0.0.1",8080)
udp=UDPService("127.0.0.1",8081)
try:
    td1=Thread(target=tcp.main)
    td2=Thread(target=udp.main)
    td1.start()
    td2.start()
    td1.join()
    td2.join()
except:
    tcp.close()
    udp.close()
finally:
    tcp.close()
    udp.close()
