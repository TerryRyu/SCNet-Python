import socket
import threading
import time

import varint
from lkcp import KcpObj

from message_header import MessageType, MAGIC_PACKET


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

        self.public_kcp_peer = None

    def is_connected():
        return True

    def set_public_kcp_peer(self, ip, port):
        self.public_kcp_peer = KcpPeer(self.sock, ip, port)

    def send(message_wrapper):

        coded_output = b''

        coded_output += MAGIC_PACKET
        coded_output += varint.encode(message_wrapper.byte_size)
        coded_output += varint.encode(message_wrapper.packet_type_num)
        coded_output += varint.encode(message_wrapper.message_type_num)
        coded_output += varint.encode(self.crypto_type)
        coded_output += varint.encode(self.connection_id)

        coded_output += message_wrapper.byte_message

        with self.public_kcp_peer.mutex:
            ret = self.public_kcp_peer.kcp.send(coded_output)

        return ret

    def recv_header():
        pass

    def recv_body():
        pass

class KcpPeer:
    def __init__(self, sock, ip, port):

        self.kcp = KcpObj(0x11223344, id(self), self)
        self.kcp.nodelay(1, 10, 2, 1)
        self.kcp.wndsize(128, 128)
        self.kcp.setmtu(1400)

        self.next = 0
        self.sock = sock

        self.server_peer = ip, port

        self.mutex = threading.Lock()

        self.last_ping = None

    def udp_output(self, data):
        return self.sock.sendto(data, self.server_peer)


if __name__ == '__main__':
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)

    sess = RendezvousSession(sock, 1)
    sess.set_public_kcp_peer(0x11223344, '127.0.0.1', 9191)

