# #coding=UTF-8

# import time
# import socket
# import random
# from lkcp import KcpObj

# g_ScriptStartTime = time.time()

# def getms():
#     return int((time.time()-g_ScriptStartTime)*1000)


# def GetMillisecond():
#     return int(time.time() * 1000)


# def udp_output(uid, data):
#     print('udp_output')
#     print(len(data))
#     for b_ in data:
#         print(b_, end=' ')
#     s.sendto(data, addr)


# def recv_udp(sock):
#     try:
#         data, udp_addr = sock.recvfrom(65535)
#         return data
#     except Exception as e:
#         pass
#     return None


# # socket连接
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.setblocking(0)
# addr = ("127.0.0.1", 9991)

# kcp = KcpObj(conv = 123, 
#              id = 1, 
#              callback = udp_output)

# kcp.nodelay(1, 10, 2, 1)
# kcp.wndsize(128, 128)
# kcp.setmtu(1000)

# start_ts = getms()  # 获取代码运行一直到此时的时间差
# slap = start_ts

# # while True:

# #     data = recv_udp(s)

# #     if data is not None:
# #         # KcpPerrMap lcok ?
# #         kcp.input(data)
# #         kcp.update(time.time())

# num_data = 0
# while True:
#     current = getms()
#     kcp.update(time.time())

#     while current >= slap:  # 发送sleep()/100次
#         # data = str(random.randint(0, 10000))
#         num_data = str(int(num_data)+1)
#         # print("Send: ", num_data)
#         kcp.send(num_data)
#         slap += 50


#     while True:
#         data = recv_udp(s)
#         if data is None:
#             break

#         print('recv_udp')
#         # print('raw_recv_udp', data)
#         kcp.input(data)

#     i = 0
#     while True:

#         lens, data = kcp.recv()

#         # core.pyx에는 <= 으로 되어 있음
#         if lens < 0:
#             break
#         # print(i, "Recv: ", data)
#         kcp.send(data)
#         i+=1

#     time.sleep(0.001)







#coding=UTF-8

import random
import socket
import time

from utils import uint322netbytes, netbytes2uint32
from lkcp import KcpObj

g_ScriptStartTime = time.time()

def getms():
    return int((time.time()-g_ScriptStartTime)*1000)


def GetMillisecond():
    return int(time.time() * 1000)


def kcp_callback(uid, data):
    s.sendto(data, addr)


def recv_udp(sock):
    try:
        data, udp_addr = sock.recvfrom(1400)
        return data
    except Exception as e:
        pass
    return None


# socket连接
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(0)
addr = ("127.0.0.1", 9191)

kcp = KcpObj(123, 1, kcp_callback)
kcp.nodelay(1, 10, 2, 1)
kcp.wndsize(128, 128)
kcp.setmtu(1400)

start_ts = getms()  # 获取代码运行一直到此时的时间差
slap = start_ts

# rList = list(range(256))*100
# print(len(rList))
# send_data = bytes(rList)

index = 0
while True:

    current = getms()
    kcp.update(current)

    while current >= slap:  # 发送sleep()/100次
        send_data = uint322netbytes(index)
        kcp.send(send_data)
        slap += 100

        print('send:', netbytes2uint32(send_data))
        index += 1

    while True:
        data = recv_udp(s)
        if data is None:
            break
        kcp.input(data)

    while True:
        lens, data = kcp.recv()
        if lens < 0:
            break

        print('     recv:', netbytes2uint32(data))
    
    print('')

    time.sleep(0.1)
