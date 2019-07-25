from utils import *

# index = 128

# s1 = uint322netbytes(index)
# print(s1.__class__)

# s2 = netbytes2uint32(s1)

# print(s2)

print(128&255)


index = 194
s1 = uint322netbytes(128)
print('len', len(s1))

print(s1.encode('utf-8'))


print(b'\x00\x00\x00\xc2')

s2 = netbytes2uint32(b'\x00\x00\x00\xc2')
print(s2)


print(chr(123123123))