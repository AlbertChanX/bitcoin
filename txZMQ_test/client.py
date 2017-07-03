# coding:utf-8

from txzmq import ZmqEndpoint, ZmqEndpointType, ZmqFactory, ZmqREQConnection, ZmqREPConnection, ZmqRequestTimeoutError
import time, zmq
from collections import namedtuple
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
import ConfigParser


conf = ConfigParser.ConfigParser()
conf.read("client.conf")
m_ip = conf.get("master", "m_ip")
s_ip = conf.get("slave", "s_ip")
# for _ in range(100):
#     # ZmqEndpoint = namedtuple('ZmqEndpoint', ['type', 'address'])
#     # ep = ZmqEndpoint._make([ZmqEndpointType.connect, 'tcp://127.0.0.1:8880'])
#     e = ZmqEndpoint('connect', 'tcp://127.0.0.1:8880')
#     s = ZmqREQConnection(zf, e)


zf = ZmqFactory()

global req
req = ZmqREQConnection(zf, ZmqEndpoint('connect', m_ip))     # .shutdown()


class Client(object):

    def __init__(self, s):
        self.s = s


if __name__ == "__main__":

    def produce():
        global req
        data = str(time.time()) + ' '   # data json 1M
        print("Requesting %r" % data)
        try:
            d = req.sendMsg(data, timeout=6)
            def doPrint(reply):  # else reply -->list
                print("Got reply: %s" % (reply))  # ???

            def onTimeout(fail):  # except
                fail.trap(ZmqRequestTimeoutError)
                print "Timeout on request, is reply server running?"
                print('switching to other worker: %s' % s_ip)
                global req
                req.shutdown()
                req = ZmqREQConnection(zf, ZmqEndpoint('connect', s_ip))
            d.addCallback(doPrint).addErrback(onTimeout)
        except zmq.error.Again:
            print("Skipping, no consumers...")
        reactor.callLater(1, produce)       # callLater(1,produce,args)  args --> produce(callback)
    reactor.callWhenRunning(produce)
    reactor.run()