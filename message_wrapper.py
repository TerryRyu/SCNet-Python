from sys import getsizeof as get_size

import varint

from message_header import MessageType, MAGIC_PACKET


class MessageWrapper:
    def __init__(self, message, registered_types):

        self.byte_message = None
        self.byte_size = None
        self.packet_type_num = None
        self.message_type_num = None
        
        self.wrap_message(message, registered_types)

    def wrap_message(self, message, registered_types):

        packet_type = type(message)

        packet_info = registered_types[packet_type]
        if packet_info is None:
            raise TypeError('You must register packet type [{}]'.
                                                format(packet_type))

        self.message_type_num = packet_info[0]
        self.packet_type_num = packet_info[1]

        """
        Specification byte size of message per all packet types
        """
        self.byte_size = None

        if self.message_type_num == MessageType.RAWBYTE:
            if packet_type is str:

                self.byte_message = message.encode('UTF-8')
                self.byte_size = len(message)

        elif self.message_type_num == MessageType.PROTOBUF:
            self.byte_message = message.SerializeToString()
            self.byte_size = message.ByteSize()

        else:
            pass

    def __repr__(self):
        repr_str = ''
        repr_str += f'message: {self.message}'
        repr_str += f'bytesize: {self.bytesize}'
        repr_str += f'message_type_num: {self.message_type_num}'
        repr_str += f'packet_type_num: {self.packet_type_num}'

        return repr_str