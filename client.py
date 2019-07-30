import socket
import time
import threading

from message_header import MAX_PACKET_SIZE
from session import RendezvousSession, KcpPeer
from utils import uint322netbytes, netbytes2uint32

g_ScriptStartTime = time.time()

def get_current_ms():
    return int((time.time()-g_ScriptStartTime)*1000)

def on_callback(rendvs_client, packet):
    # print(rendvs_client)
    print('on_callback:',netbytes2uint32(packet))

    '''
    read_header
    read_raw_body

    message parse ...

    '''


class RendezvousClient:
    def __init__(self, ip, port, if_name, serial):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        # self.sock.settimeout(1)

        self.if_name = if_name
        # self.rendvs_server_kcp_peer = KcpPeer(self.sock, ip, port)

        self.register_thread = None
        self.recv_thread = RecvThread(self)
        self.raw_recv_thread = RawRecvThread(self)

        self.kcp_peer_map = None
        self.mutex_for_kcp_peer_map = None

        self.rendvs_sess_map = None
        self.mutex_for_rendvs_sess_map = None

        self.last_registration_time = None

        self.rendvs_sess = RendezvousSession(self.sock, 0)
        self.rendvs_sess.set_public_kcp_peer(ip, port)

        self.on_server_connecting = None
        self.on_server_connect_failed = None
        self.on_server_connected = None
        self.on_server_disconnected = None

        self.on_connecting_callback = None
        self.on_connected_callback = None
        self.on_connection_target_invalid_callback = None
        self.on_connection_id_created_callback = None
        self.on_connected_failed_callback = None

    def start(self):
        print('start')
        self.raw_recv_thread.start()
        self.recv_thread.start()
    
    def stop(self):
        print('stop')
        self.raw_recv_thread.interrupt()
        self.recv_thread.interrupt()
        

class StoppableThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def interrupt(self):
        self._stop_event.set()

    def is_interrupted(self):
        return self._stop_event.is_set()


class RawRecvThread(StoppableThread):
    def __init__(self, rendvs_client):
        super().__init__()
        self.rendvs_client = rendvs_client

        print('init raw_recv')

    def recv_udp(self):
        try:
            data, udp_addr = self.rendvs_client.sock.recvfrom(1000)
            return data, udp_addr
        except Exception as e:
            print(e)

        return None, None

    def run(self):
        print('run raw_recv')
        kcp_peer = self.rendvs_client.rendvs_sess.public_kcp_peer
        while not self.is_interrupted():
            data, udp_addr = self.recv_udp()
            if data is not None:
                with kcp_peer.mutex:
                    kcp_peer.kcp.input(data)
                    kcp_peer.kcp.update(get_current_ms())

            time.sleep(0.01)


class RecvThread(StoppableThread):
    def __init__(self, rendvs_client):
        super().__init__()
        self.rendvs_client = rendvs_client
        print('init recv')

    def run(self):
        print('run recv')
        kcp_peer = self.rendvs_client.rendvs_sess.public_kcp_peer
        while not self.is_interrupted():

            with kcp_peer.mutex:
                len_, data = kcp_peer.kcp.recv()
                kcp_peer.kcp.update(get_current_ms())

            if len_ > 0:
                on_callback(self.rendvs_client, data)

            time.sleep(0.01)


if __name__ == '__main__':

    client = RendezvousClient('127.0.0.1', 50001, 'test', 0)
    client.start()

    cnt = 300
    while cnt >= 0:
        with client.rendvs_sess.public_kcp_peer.mutex:
            client.rendvs_sess.public_kcp_peer.kcp.send(
                            cnt.to_bytes(4, byteorder="big", signed=False))
            client.rendvs_sess.public_kcp_peer.kcp.update(get_current_ms())

            cnt-=1

        time.sleep(0.01)
