import threading
import logging
import random
import time


g_ScriptStartTime = time.time()
g_RndSeed = int(time.time())

log = logging.getLogger(__name__)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

log.addHandler(handler)
log.setLevel(logging.DEBUG)


def msleep(ms):
    time.sleep(ms * 0.001)

def initrndseed():
    global g_RndSeed
    random.seed(g_RndSeed)

def rndvalue(_min, _max):
    return _min + random.randint(0, _max - _min)
    # return random.randint(0, _max - _min)

def getms():
    global g_ScriptStartTime
    return int((time.time()-g_ScriptStartTime)*1000)

def uint322netbytes(i):
    # a, b, c, d = chr(i>>24&255) ,chr(i>>16&255),chr(i>>8&255),chr(i&255)
    # print(a.encode('utf-8'))
    # print(b.encode('utf-8'))
    # print(c.encode('utf-8'))
    # print(d.encode('utf-8'))

    # return chr(i>>24&255) + chr(i>>16&255) + chr(i>>8&255) + chr(i&255)
    return i.to_bytes(4, byteorder="big", signed=False)

def netbytes2uint32(s):
    # return s[0]<<24 | s[1]<<16 | s[2]<<8 | s[3]
    return int.from_bytes(s, byteorder="big", signed=False)

def make_enum(type_name='Enum', start=0, *sequential, **named):
    enums = dict(zip(sequential, range(start, start+len(sequential))), **named)
    return type(type_name, (), enums)

def get_current_time_sec():
    return time.time()

class StoppableThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def interrupt(self):
        self._stop_event.set()

    def is_interrupted(self):
        return self._stop_event.is_set()
