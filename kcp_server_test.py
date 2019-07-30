import socket
import time

from session import KcpPeer
from utils import uint322netbytes, netbytes2uint32

g_ScriptStartTime = time.time()

def getms():
    return int((time.time()-g_ScriptStartTime)*1000)

def recv_udp(sock):
    try:
        data, udp_addr = sock.recvfrom(1400)
        return data, udp_addr
    except Exception as e:
        pass
    return None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('127.0.0.1', 50001)
sock.bind(addr)

data, udp_addr = recv_udp(sock)

kcp_peer = KcpPeer(sock, *udp_addr)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setblocking(False)

while True:

    current = getms()
    kcp_peer.kcp.update(current)

    while True:
        data, addr = recv_udp(sock)
        if data is None:
            break

        kcp_peer.kcp.input(data)

    while True:
        len_, data = kcp_peer.kcp.recv()
        if len_ < 0:
            break

        print('echo send:', netbytes2uint32(data))
        kcp_peer.kcp.send(data)
        # kcp_peer.kcp.send(uint322netbytes(300))

    time.sleep(0.01)
