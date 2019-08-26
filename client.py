import socket
import time
import threading


from message_header import MAX_PACKET_SIZE
from message_header import SEPERATOR
from message_header import MessageType
from message_header import parse_data
from message_wrapper import MessageWrapper
from session import RendezvousSession, KcpPeer
from session import send_message
from rendevous_message import RendezvousMessage as RM
from utils import log
from utils import uint322netbytes, netbytes2uint32
from utils import get_current_time_sec
from utils import threading


g_ScriptStartTime = time.time()

def get_ip_address(sock):
    sock.connect(('8.8.8.8', 80))
    return sock.getsockname()

def get_current_ms():
    return int((time.time()-g_ScriptStartTime)*1000)

def on_callback(rendvs_client, kcp_peer, buff, recv_size):
    parsed = parse_data(buff)
    if not parsed:
        return

    msg_header = parsed[0]
    msg_body = parsed[1]

    reg_types = rendvs_client.registered_types
    
    msg_type = message_header.message_type
    pkt_type = message_header.packet_type

    # getms로 해도 되나?
    kcp_peer.last_ping = get_current_time_sec()
    if msg_type == MessageType.PROTOBUF:
        PacketClass, callback_func = reg_types[(msg_type, pkt_type)]

        if PacketClass is None:
            log.info('Unknown protobuf packet_type {pkt_type} received')
            return

        rendvs_sess = get_rendvs_sess_safety(rendvs_client, message_header)

        message = PacketClass() 
        message.ParseFromString(msg_body)

        if callback_func is not None:
            log.debug('run callback_func')
            callback_func(rendvs_sess, message)
        else:
            log.warning("There's no callback function")

        return

    elif msg_type == MessageType.RAWBYTE:
        if pkt_type < RM.REGISTRATION_RENDEZVOUS_CLIENT_REQUEST:
            rendvs_sess = get_rendvs_sess_safety(rendvs_client, message_header)
            _, callback_func = reg_types[(msg_type, pkt_type)]

            if callback_func is not None:
                log.debug('run callback_func')
                callback_func(rendvs_sess, msg_body, message_header.byte_size)
            else:
                log.warning(f"unregistered raw message received. {msg_body}")

        return

    if msg_type != MessageType.RAWBYTE
        log.warning(f"unregistered message_type received. {msg_type}")
        return


    # if pkt_type == RM.REGISTRATION_RENDEZVOUS_CLIENT_SUCCESS:


    '''
    read_header
    read_raw_body

    message parse ...

    '''

def create_udp_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)

    return sock


class RendezvousClient:
    def __init__(self, ip, port, serial, registered_types):

        self.registered_types = registered_types

        self.sock = create_udp_socket()

        self.register_thread = RegisterThread(self)
        self.recv_thread = RecvThread(self)
        self.raw_recv_thread = RawRecvThread(self)

        self.kcp_peer_map = {}
        self.rendvs_sess_map = {}
        self.mutex_for_kcp_peer_map = threading.Lock()
        self.mutex_for_rendvs_sess_map = threading.Lock()

        self.server_ip = ip
        self.server_port = port
        self.serial = serial
        self.is_connected = False

        self.on_server_connecting = None
        self.on_server_connect_failed = None
        self.on_server_connected = None
        self.on_server_disconnected = None

        self.on_connecting = None
        self.on_connected = None
        self.on_connection_target_invalid = None
        self.on_connection_id_created = None
        self.on_connected_failed = None
        self.on_disconnected = None

    def start(self):
        log.info('Rendezvous client start...')

        self.register_thread.start()
        self.raw_recv_thread.start()
        self.recv_thread.start()
    
    def stop(self):
        log.info('Rendezvous client stop...')

        self.register_thread.interrupt()
        self.raw_recv_thread.interrupt()
        self.recv_thread.interrupt()

        # clear 추가
        
    def get_rendvs_sess_safety(self, message_header):
        c_id = message_header.connection_id
        if len(self.rendvs_sess_map[c_id]) == 0:
            rendvs_sess = RendezvousSession(self.sock, c_id)

            if c_id != 0:
                self.rendvs_sess_map[c_id] = rendvs_sess
            else:
                server_peer = Peer(self.client.server_ip, 
                                   self.client.server_port)
                rendvs_sess.public_kcp_peer = self.get_kcp_peer(server_peer)

            return rendvs_sess

        return self.rendvs_sess_map[c_id]

    def get_kcp_peer(self, peer):
        """
        Key 중복되어도 되나 확인 필요
        중복이 가능할 경우 value를 list로 변경할 예정
        """
        if len(self.kcp_peer_map[peer.key]) == 0:
            kcp_peer = KcpPeer(self.sock, peer.ip, peer.port)
        else:
            kcp_peer = self.kcp_peer_map[peer.key]

        return kcp_peer

class RegisterThread(StoppableThread):
     def __init__(self, client):
        super().__init__()

        log.debug('init register thread...')
        self.client = client

    def run(self):

        local_ip, local_port = get_ip_address()
        log.info(f'local IP Address: {local_ip}, {local_port}')

        message = local_ip + SEPERATOR \
                    + str(local_port) + SEPERATOR \
                    + self.client.serial

        TIMEOUT_S = 60
        PING_INTERVAL_S = 30
        LOOP_INTERVAL_S = 5
        conn_flag = False

        server_peer = Peer(self.client.server_ip, self.client.server_port)
        while not self.is_interrupted():
            current_time = get_current_time_sec()
            with self.client.mutex_for_kcp_peer_map:
                for kcp_peer in list(self.kcp_peer_map.values()):
                    if kcp_peer.last_ping + TIMEOUT_S < current_time:
                        if kcp_peer.peer == server_peer:
                            continue

                        log.info(f'removed kcp_peer: {kcp_peer.peer.key}')
                        del self.kcp_peer_map[kcp_peer.peer.key]

                    elif kcp_peer.last_ping + PING_INTERVAL_S < current_time:
                        message_wrapper = MessageWrapper(
                            registered_types=self.client.registered_types,
                            message=None,
                            message_type=MessageType.RAWBYTE,
                            packet_type=RM.PING_REQUEST,
                            connection_id=0)

                        kcp_peer.send(message_wrapper)

            with self.client.mutex_for_rendvs_sess_map:
                for key, rendvs_sess in list(self.rendvs_sess_map.items()):
                    if rendvs_sess is None:
                        continue

                    if rendvs_sess.relay_kcp_peer is not None:
                        last_ping = rendvs_sess.relay_kcp_peer.last_ping
                        if last_ping + TIMEOUT_S < current_time:
                            log.warning(f'relay peer removed, {last_ping}')
                            rendvs_sess.relay_kcp_peer = None

                    if rendvs_sess.public_kcp_peer is not None:
                        last_ping = rendvs_sess.public_kcp_peer.last_ping
                        if last_ping + TIMEOUT_S < current_time:
                            log.warning(f'public peer removed, {last_ping}')
                            rendvs_sess.public_kcp_peer = None

                    if rendvs_sess.private_kcp_peer is not None:
                        last_ping = rendvs_sess.private_kcp_peer.last_ping
                        if last_ping + TIMEOUT_S < current_time:
                            log.warning(f'private peer removed, {last_ping}')
                            rendvs_sess.private_kcp_peer = None

                    if not rendvs_sess.is_connected():
                        del self.rendvs_sess_map[key]

                        if self.client.on_disconnected is not None:
                            self.client.on_disconnected(rendvs_sess)

                        log.info(f'Disconnected, connectionID=\
                                        {rendvs_sess.connection_id}')

            if not self.client.is_connected:
                if conn_flag:
                    with self.client.mutex_for_kcp_peer_map:
                        del self.client.kcp_peer_map[server_peer.key]
                    self.client.sock = create_udp_socket()
                    self.client.on_server_connect_failed()

                else:
                    conn_flag = True

                self.client.on_server_connecting()

                message_wrapper = MessageWrapper(
                    registered_types=self.client.registered_types,
                    message=message,
                    message_type=MessageType.RAWBYTE,
                    packet_type=RM.REGISTRATION_RENDEZVOUS_CLIENT_REQUEST,
                    connection_id=0)

                self.client.get_kcp_peer(server_peer).send(message_wrapper)

            elif self.client.get_kcp_peer(server_peer).last_ping \
                    + TIMEOUT_S < current_time:
                
                with self.client.mutex_for_kcp_peer_map:
                    del self.client.kcp_peer_map[server_peer.key]

                conn_flag = False
                self.client.is_connected = False
                self.client.sock = create_udp_socket()
                self.client.on_server_disconnected()

            else:
                message_wrapper = MessageWrapper(
                    registered_types=self.client.registered_types,
                    message=message,
                    message_type=MessageType.RAWBYTE,
                    packet_type=RM.REGISTRATION_RENDEZVOUS_CLIENT_REQUEST,
                    connection_id=0)

                self.client.get_kcp_peer(server_peer).send(message_wrapper)

            time.sleep(LOOP_INTERVAL_S)

        log.debug('registerThread finished')

        return 


class RawRecvThread(StoppableThread):
    def __init__(self, client):
        super().__init__()

        log.debug('init raw recv thread...')
        self.client = client

    def recv_udp(self):
        try:
            data, udp_addr = self.client.sock.recvfrom(MAX_PACKET_SIZE)
            return data, udp_addr
        except Exception as e:
            pass
            # print(e)

        return None, None

    def run(self):
        log.debug('run raw recv thread...')
        kcp_peer = self.client.rendvs_sess.public_kcp_peer
        while not self.is_interrupted():
            data, udp_addr = self.recv_udp()
            if data is not None:
                with kcp_peer.mutex:
                    kcp_peer.kcp.input(data)
                    kcp_peer.kcp.update(get_current_ms())

            time.sleep(0.01)


class RecvThread(StoppableThread):
    def __init__(self, client):
        super().__init__()
        log.debug('init recv thread...')
        self.client = client
        
    def run(self):
        log.debug('run recv thread...')
        kcp_peer = self.client.rendvs_sess.public_kcp_peer
        while not self.is_interrupted():

            with kcp_peer.mutex:
                len_, data = kcp_peer.kcp.recv()
                kcp_peer.kcp.update(get_current_ms())

            if len_ > 0:
                on_callback(self.client, data)

            time.sleep(0.01)


if __name__ == '__main__':

    client = RendezvousClient('127.0.0.1', 50001, 'test', 0)
    client.start()

    cnt = 100
    while cnt >= 0:
        with client.rendvs_sess.public_kcp_peer.mutex:
            client.rendvs_sess.public_kcp_peer.kcp.send(
                            cnt.to_bytes(4, byteorder="big", signed=False))
            client.rendvs_sess.public_kcp_peer.kcp.update(get_current_ms())

            cnt-=1

        time.sleep(0.01)

    time.sleep(1)
    client.stop()
