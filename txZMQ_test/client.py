# coding:utf-8

from txzmq import ZmqEndpoint, ZmqFactory, ZmqREQConnection, ZmqREPConnection, ZmqRequestTimeoutError
import time, zmq

from twisted.internet import reactor


zf = ZmqFactory()
e = ZmqEndpoint('connect', 'tcp://127.0.0.1:8880')

s = ZmqREQConnection(zf, e)

def produce():
    data = str(time.time())
    print "Requesting %r" % data
    try:
        d = s.sendMsg(data, timeout=0.95)

        def doPrint(reply):    # else reply -->list
            print("Got reply: %s" % (reply[0]))   # ???

        def onTimeout(fail):   # except
            fail.trap(ZmqRequestTimeoutError)
            print "Timeout on request, is reply server running?"

        d.addCallback(doPrint).addErrback(onTimeout)
    except zmq.error.Again:
        print "Skipping, no consumers..."

    reactor.callLater(1, produce)    # callLater(1,produce,args)  args --> produce

reactor.callWhenRunning(reactor.callLater, 1, produce)

reactor.run()