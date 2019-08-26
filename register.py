from collections import defaultdict
from pprint import pprint

from message_header import MessageType

class MessageTypeRegisterer:
    def __init__(self):

        self.registered_types = defaultdict(lambda: (None, None))

    def register(self, message_type, packet_class, packet_type, callback):
        if not isinstance(packet_class, type):
            raise TypeError(f'{{packet_class}} is invalid type')

        if packet_type < 0:
            raise ValueError(f'{{packet_type}} is invalid num')

        for pk_cls, _ in self.registered_types.items():
            if pk_cls == packet_class:
                raise TypeError('f{{packet_class}} is already registered')

        self.registered_types[(message_type, packet_type)] = \
                                            [packet_class, callback]
    
    def register_protobuf(self, packet_class, packet_type, callback=None):
        self.register(MessageType.PROTOBUF, packet_class, packet_type)

    def register_raw_byte(self, packet_type, callback=None):
        self.register(MessageType.RAWBYTE, None, packet_type)


if __name__ == '__main__':
    registerer = MessageTypeRegisterer()

    registerer.register_raw_byte(0, lambda x: x+1)

# class MessageTypeRegisterer:
#     def __init__(self):

#         self.registered_types = defaultdict(lambda: defaultdict(lambda: -1))

#     def register(self, message_type, packet_type, packet_type_num, 
#                                                   call_back=None):

#         if not isinstance(packet_type, type):
#             raise TypeError('\'{}\' is invalid type'.format(packet_type))

#         elif packet_type_num < 0:
#             raise ValueError('\'{}\' is invalid num'.format(packet_type_num))
        
#         else:
#             self.registered_types[message_type][packet_type] = packet_type_num

#     def register_protobuf(self, packet_type, packet_type_num, call_back=None):
#         self.register(MessageType.PROTOBUF, packet_type, packet_type_num)

#     def register_raw_byte(self, packet_type, packet_type_num, call_back=None):
#         self.register(MessageType.RAWBYTE, packet_type, packet_type_num)


# if __name__ == '__main__':
#     registerer = MessageTypeRegisterer()

#     registerer.register_raw_byte(str, 0)