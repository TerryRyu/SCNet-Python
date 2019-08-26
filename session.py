import socket
import threading
import time

import varint
from lkcp import KcpObj

from message_header import MessageType, MAGIC_PACKET
from message_wrapper import MessageWrapper
from utils import get_current_time_sec


class BaseSession:
    def send(message):
        raise NotImplementedError()

    def recv_header():
        raise NotImplementedError()

    def recv_body():
        raise NotImplementedError()


class RendezvousSession(BaseSession):
    
    def __init__(self, sock, connection_id):
        self.sock = sock
        self.connection_id = connection_id
        self.crypto_type = 0

        self.private_kcp_peer = None
        self.public_kcp_peer = None
        self.relay_kcp_peer = None

    def is_connected(self):
        if self.private_kcp_peer is not None \
                or self.public_kcp_peer is not None \
                or self.relay_kcp_peer is not None:

            return True

        return False

    def recv_header():
        pass

    def recv_body():
        pass

class KcpPeer:
    def __init__(self, sock, ip, port):

        self.peer = Peer(ip, port)

        self.kcp = KcpObj(0x11223344, id(self), self)
        self.kcp.nodelay(1, 10, 2, 1)
        self.kcp.wndsize(128, 128)
        self.kcp.setmtu(1400)

        self.sock = sock
        self.mutex = threading.Lock()

        self.next = 0
        self.last_ping = get_current_time_sec()

    def udp_output(self, data):
        return self.sock.sendto(data, (self.peer.ip, self.peer.port))

    def send(self, message_wrapper):

        if not isinstance(message_wrapper, MessageWrapper):
            return False

        with kcp_peer.mutex:
            result = kcp_peer.kcp.send(message_wrapper.get_coded_output())

        return result

class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.key = f'{self.ip}:{self.port}'

    def __eq__(self, other):
        return self.key == other.key

if __name__ == '__main__':

    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.setblocking(False)

    # sess = RendezvousSession(sock, 1)
    # sess.set_public_kcp_peer(0x11223344, '127.0.0.1', 9191)

