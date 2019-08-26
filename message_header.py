from utils import make_enum
import varint

MAGIC_PACKET = b'IJ'
MAGIC_PACKET_LENGTH = 2

HEADER_ELEMENTS_NUM = 5
MAX_PACKET_HEADER_SIZE = 7 * HEADER_ELEMENTS_NUM

MAX_PACKET_SIZE = 655350
MAX_WAIT_SEND_MS = 1000

SEPERATOR = ' '

MessageType = make_enum('MessageType', 0, 
    'PROTOBUF',
    'RAWBYTE',
    'RAWBYTE_RELAY',
    'PROTOBUF_RELAY')

# recv 시에 사용?
class MessageHeader:
    def __init__(self, data_size,
                       packet_type,
                       message_type,
                       crypt_type,
                       connection_id):

        self.byte_size = byte_size
        self.packet_type = packet_type
        self.message_type = message_type
        self.crypt_type = crypt_type
        self.connection_id = connection_id

    def __repr__(self):

        ret_string = ''
        ret_string += 'byte_size = %d\n' % self.byte_size
        ret_string += 'packet_type = %d\n' % self.packet_type
        ret_string += 'message_type = %d\n' % self.message_type
        ret_string += 'crypt_type = %d\n' % self.crypt_type
        ret_string += 'connection_id = %d' % self.connection_id

        return ret_string

def parse_data(buff):

    if len(buff) < MAGIC_PACKET_LENGTH + HEADER_ELEMENTS_NUM:
        return False

    if buf[:MAGIC_PACKET_LENGTH] != MAGIC_PACKET:
        return False

    decoded_data_list = []
    s = MAGIC_PACKET_LENGTH
    e = MAGIC_PACKET_LENGTH
    element_count = 0
    while True:
        if serial_data[e] <= 127: # int
            
            b = serial_data[s:e+1] # slicing to parse byte data
            if isinstance(b, bytes):
                decoded_data = varint.decode_bytes(b)
                decoded_data_list.append(decoded_data)
                s = e + 1
                element_count += 1
            else:
                # something to do like handling error
                return False

        if element_count == HEADER_ELEMENTS_NUM:
            break
            
        e += 1

    message_header = MessageHeader(*decoded_data_list)
    message_body = serial_data[s:]

    return message_header, message_body


if __name__ == '__main__':
    
    print(MessageType.PROTOBUF)