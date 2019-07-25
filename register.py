from collections import defaultdict
from pprint import pprint

from message_header import MessageType

class MessageTypeRegisterer:
    def __init__(self):

        self.registered_types = defaultdict(lambda: None)

    def register(self, message_type_num, packet_type, packet_type_num, 
                                                      call_back=None):
        if not isinstance(packet_type, type):
            raise TypeError('\'{}\' is invalid type'.format(packet_type))

        elif packet_type_num < 0:
            raise ValueError('\'{}\' is invalid num'.format(packet_type_num))

        else:
            # callback을 튜플에 추가?
            self.registered_types[packet_type] = (message_type_num,
                                                  packet_type_num)

            # self.registered_types[(message_type_num, packet_type_num)] = \
            #                                             packet_type



    def register_protobuf(self, packet_type, packet_type_num, call_back=None):
        self.register(MessageType.PROTOBUF, packet_type, packet_type_num)

    def register_raw_byte(self, packet_type, packet_type_num, call_back=None):
        self.register(MessageType.RAWBYTE, packet_type, packet_type_num)


if __name__ == '__main__':
    registerer = MessageTypeRegisterer()

    registerer.register_raw_byte(str, 0)

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