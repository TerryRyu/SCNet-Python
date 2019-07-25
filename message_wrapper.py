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

                # message에 따로 NULL값을 추가해야하나?
                self.byte_message = message.encode('UTF-8')
                self.byte_size = len(message)

                # str일 경우 length로 해야하나? getsizeof로 해야하나?
                # C++이랑 bytesize가 다를 수 있기 때문에..
                #   => 파이썬에서는 send할 때 byte data만 보내는것 확인했음
                #   => so, byte_size를 len으로 처리하면 될 듯
                #   => 이때 message에 NULL을 넣어야 하는지?

                # self.byte_size = get_size(self.byte_message)

        elif self.message_type_num == MessageType.PROTOBUF:
            self.byte_message = message.SerializeToString()
            self.byte_size = message.ByteSize()

            # need message serialize to string(byte) ?
            # self.byte_message = message

        else:
            pass


    def encode_to_bytes(self):

        coded_output = b''

        coded_output += MAGIC_PACKET
        coded_output += varint.encode(self.byte_size)
        coded_output += varint.encode(self.packet_type_num)
        coded_output += varint.encode(self.message_type_num)
        coded_output += varint.encode(0)
        coded_output += varint.encode(0)

        coded_output += self.byte_message

        return coded_output


    def print_attrs(self):
        print('message:', self.message)
        print('bytesize', self.byte_size)
        print('message_type_num:', self.message_type_num)
        print('packet_type_num:', self.packet_type_num)
        