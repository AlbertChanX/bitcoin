# coding:utf-8

from txzmq import ZmqEndpoint, ZmqFactory, ZmqPubConnection, ZmqSubConnection
from twisted.internet import reactor
import time

zf = ZmqFactory()
global sub
sub1 = ZmqSubConnection(zf, ZmqEndpoint('connect', 'tcp://127.0.0.1:8881'))
sub1.subscribe("btc")
sub2 = ZmqSubConnection(zf, ZmqEndpoint('connect', 'tcp://127.0.0.1:10001'))
sub2.subscribe("btc")


def doPrint(*args):   # gotMessage(self, message, tag):
    print("interval: %s" % (time.time()-float(args[0])))
    print("message received: %r" % (args,))
sub1.gotMessage = doPrint
sub2.gotMessage = doPrint

reactor.run()