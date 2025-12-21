import socket
from io import *


class SocketIO(IOBase):
    def __init__(self):
        self.data = b''
        self.pos = 0

    def send(self, data):
        self.data += data

    def recv(self, size, flags=0):
        self.pos += size
        data = self.data[self.pos - size:self.pos]
        if flags & socket.MSG_PEEK:
            self.pos -= size

        return data
