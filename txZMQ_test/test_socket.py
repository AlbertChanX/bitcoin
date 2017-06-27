# coding:utf-8
import zmq
import sys
import time
import uuid
from time import sleep
port = '5555'
# port,port1,client_name= sys.argv[1:]  

context = zmq.Context()
print(context.get(1))
print(context.get(2))

context.set(zmq.MAX_SOCKETS, 10000)
context.set(zmq.IO_THREADS, 100)
print(context.get(1))
print(context.get(2))

global socket
socket = context.socket(zmq.REQ)


def getNextId():
    return uuid.uuid4().bytes


class Client(object):
    """docstring for  """

    def __init__(self, socket):
        self.socket = socket
        self.socket.connect('tcp://localhost:%s' % port)

    def request(self):
        id = getNextId()
        data = [id, b''] + [b'wfw']
        self.socket.send(str(time.time()))
        msg = self.socket.recv()
        print msg


def generate_c():
    c = []
    for i in range(9999):
        print(i)
        global socket
        socket = context.socket(zmq.REQ)
        c.append(Client(socket))

    return c


for i in generate_c():
      i.request()
