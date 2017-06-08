# coding:utf-8
from txzmq import ZmqEndpoint, ZmqEndpointType, ZmqFactory, ZmqPushConnection, ZmqPullConnection, ZmqDealerConnection
import zmq
import time
from twisted.internet import reactor


zf = ZmqFactory()

backend = ZmqEndpoint('connect', 'tcp://127.0.0.1:8880')
frontend = ZmqEndpoint('bind', 'tcp://127.0.0.1:8881')


recv = ZmqPullConnection(zf, backend)
sender = ZmqPushConnection(zf, frontend)
while True:
    def doPrint(message):
        print "get %r" % (message,)
        try:
            data = message
            sender.push(data)
            time.sleep(1)
        except zmq.error.Again:
            print "Skipping, no pull consumers..."
    recv.onPull = doPrint

if __name__ == "__main__":
    pass







