from enum import Enum

MAGIC_PACKET = b'IJ'
MAGIC_PACKET_LENGTH = 2

HEADER_ELEMENTS_NUM = 5
MAX_PACKET_HEADER_SIZE = 7 * HEADER_ELEMENTS_NUM

MAX_PACKET_SIZE = 655350
MAX_WAIT_SEND_MS = 1000

# enum 스타일로 변경 방법?
class MessageType:
    PROTOBUF = 0
    RAWBYTE = 1
    RAWBYTE_RELAY = 2
    PROTOBUF_RELAY = 3

# recv 시에 사용?
class MessageHeader:
    def __init__(self, byte_size,
                       packet_type_num,
                       message_type_num,
                       crypt_type,
                       connection_id):

        self.byte_size = byte_size
        self.packet_type_num = packet_type_num
        self.message_type_num = message_type_num
        self.crypt_type = crypt_type
        self.connection_id = connection_id

    def __repr__(self):

        ret_string = ''
        ret_string += 'byte_size = %d\n' % self.byte_size
        ret_string += 'packet_type_num = %d\n' % self.packet_type_num
        ret_string += 'message_type_num = %d\n' % self.message_type_num
        ret_string += 'crypt_type = %d\n' % self.crypt_type
        ret_string += 'connection_id = %d' % self.connection_id

        return ret_string


if __name__ == '__main__':
    
    print(MessageType.__dict__)