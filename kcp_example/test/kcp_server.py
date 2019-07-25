# #coding=UTF-8

# import socket
# import time
# from lkcp import KcpObj


# # send回调函数
# def kcp_callback(uid, data):
#     s.sendto(data, uid_addr[uid])

# def recv_udp(sock):
#     try:
#         data, udp_addr = sock.recvfrom(65535)
#         uid_addr[1] = udp_addr
#         return data
#     except Exception as e:
#         pass
#     return None

# # socket连接
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.setblocking(0)
# addr = ("127.0.0.1", 9991)
# s.bind(addr)

# # 存放连接客户端字典
# uid_addr = {}
# kcp = KcpObj(123, 1, kcp_callback)

# kcp.nodelay(1, 10, 2, 1)
# kcp.wndsize(128, 128)
# kcp.setmtu(1000)

# while True:
#     kcp.update(time.time())

#     while True:
#         data = recv_udp(s) 
#         if data is None:
#             break
#         kcp.input(data)

#     i = 0
#     while True:
#         lens, data = kcp.recv()
#         if lens < 0:
#             break
#         print(i, "Recv: ", data)
#         kcp.send(data)
#         i+=1

#     time.sleep(0.001)

#coding=UTF-8

import socket
import time
from lkcp import KcpObj

g_ScriptStartTime = time.time()

from utils import uint322netbytes, netbytes2uint32

def getms():
    return int((time.time()-g_ScriptStartTime)*1000)

# send回调函数
def kcp_callback(uid, data):
    s.sendto(data, uid_addr[uid])

def recv_udp(sock):
    try:
        data, udp_addr = sock.recvfrom(1400)
        uid_addr[1] = udp_addr
        return data
    except Exception as e:
        pass
    return None

# socket连接
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(0)
addr = ("127.0.0.1", 9191)
s.bind(addr)

# 存放连接客户端字典
uid_addr = {}
kcp = KcpObj(123, 1, kcp_callback)

kcp.nodelay(1, 10, 2, 1)
kcp.wndsize(128, 128)
kcp.setmtu(1400)

rList = list(range(256))*100
refer_data = bytes(rList)

while True:
    # kcp.update(time.time())
    current = getms()
    kcp.update(current)

    while True:
        data = recv_udp(s)
        if data is None:
            break

        # print('raw_recv:', len(data))
        kcp.input(data)

    while True:
        lens, data = kcp.recv()
        if lens < 0:
            break
        # print("Recv: ", data)

        print('send:', netbytes2uint32(data))
        kcp.send(data)
        
    time.sleep(0.01)
