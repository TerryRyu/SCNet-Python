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
    
    def __init__(sock, connection_id):
        self.sock = sock
        self.connection_id = connection_id
        self.crypto_type = 0

        self.public_kcp_peer = None

    def is_connected():
        return True

    def set_public_kcp_peer(kcp_conv, ip, port, udp_output):
        self.public_kcp_peer = KcpPeer(kcp_conv, 
                                       self.sock, ip, port, 
                                       udp_output)

    def send(message_wrapper):

        coded_output = b''

        coded_output += MAGIC_PACKET
        coded_output += varint.encode(message_wrapper.byte_size)
        coded_output += varint.encode(message_wrapper.packet_type_num)
        coded_output += varint.encode(message_wrapper.message_type_num)
        coded_output += varint.encode(self.crypto_type)
        coded_output += varint.encode(self.connection_id)

        coded_output += message_wrapper.byte_message

        with self.kcp_peer.mutex:
            self.kcp_peer.kcp.send(coded_output)

        return True

class KcpPeer:
    def __init__(self, kcp_conv, sock, ip, port, udp_output):

        self.kcp = KcpObj(self, kcp_conv, id(self))
        self.kcp.nodelay(1, 10, 2, 1)
        self.kcp.wndsize(128, 128)
        self.kcp.setmtu(1400)

        self.next = 0
        self.sock = sock
        self.peer = (ip, port)

        self.mutex = threading.Lock()

        self.last_ping = None

        self.callback = udp_output


if __name__ == '__main__':
    # kcp = KcpPeer(123, 1,2,3, udp_output)
    # time.sleep(3)
    # print(1)
