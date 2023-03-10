import socket
import os
def get_netstate()->bool:
    res=os.system("ping www.baidu.com")
    if res:
        return False
    else:
        return True


def get_ip()->str:
    '''获取ip地址'''
    sk=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        sk.connect(("10.255.255.255",1))
        ip=sk.getsockname()[0]
    except Exception as e:
        ip="127.0.0.1"
        raise e
    finally:
        return ip


