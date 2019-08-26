from sys import getsizeof as get_size

import varint

from message_header import MessageType, MAGIC_PACKET


class MessageWrapper:
    def __init__(self, registered_types, 
                       message, message_type, byte_size=None, packet_type=None,
                       crypto_type=0, connection_id=0):
        
        self.registered_types = registered_types

        if message_type == MessageType.RAWBYTE:
            if packet_type is None:
                raise Error('packet type must be defined')

            if isinstance(message, str):
                byted_message = message.encode('UTF-8')
            elif isinstance(message, bytes):
                byted_message = message
            elif message is None:
                byted_message = b''
            else:
                raise Error('Unknown RAWBYTE type')

            if byte_size is None:
                byte_size = len(byted_message)

        elif message_type == MessageType.PROTOBUF:
            if packet_type is None:
                packet_type = self.get_protobuf_packet_type(message.__class__)

            byted_message = message.SerializeToString()
            byte_size = message.ByteSize()

        else:
            raise Error('Unknown message type')

        self.byte_size = byte_size
        self.packet_type = packet_type
        self.message_type = message_type
        self.crypto_type = crypto_type
        self.connection_id = connection_id
        self.byted_message = byted_message

    def get_protobuf_packet_type(self, message_class):


        return 0

    def get_coded_output(self):
        coded_output = b''
        coded_output += MAGIC_PACKET
        coded_output += varint.encode(self.byte_size)
        coded_output += varint.encode(self.packet_type)
        coded_output += varint.encode(self.message_type)
        coded_output += varint.encode(self.crypto_type)
        coded_output += varint.encode(self.connection_id)
        coded_output += byted_message

        return coded_output

    def __repr__(self):

        repr_str = ''
        repr_str += f'byte_size: {self.byte_size}'
        repr_str += f'packet_type: {self.packet_type}'
        repr_str += f'message_type: {self.message_type}'
        repr_str += f'crypto_type: {self.crypto_type}'
        repr_str += f'connection_id: {self.connection_id}'
        repr_str += f'byted_message: {self.byted_message}'

        return repr_str