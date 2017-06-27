from txzmq import ZmqEndpoint, ZmqREQConnection, ZmqRequestTimeoutError
from twisted.internet import reactor
import time
import zmq
from ZmqFactory import ZmqFactory

ip = 'tcp://10.10.0.65:8880'
zf = ZmqFactory()
s = ZmqREQConnection(zf, ZmqEndpoint('connect', ip))


num = 0

class Client(object):
    def __init__(self, s):
        self.s = s

    def request(self):
        def produce():
            data = str(time.time())
            print("Requesting %r" % data)
            try:
                global num
                num += 1
                print('the num of request: %d' %num)
                d = self.s.sendMsg(data, timeout=60)

                def doPrint(reply):  # else reply -->list
                    print("Got reply: %s" % (reply[0]))  # ???

                def onTimeout(fail):  # except
                    fail.trap(ZmqRequestTimeoutError)
                    print("Timeout on request, is reply server running?")

                d.addCallback(doPrint).addErrback(onTimeout)
            except zmq.error.Again:
                print("Skipping, no consumers...")
            reactor.callLater(10, produce)
        reactor.callWhenRunning(produce)


def generate_c():
    c_list = []
    for i in range(100):
        print(i)
        global s
        s = ZmqREQConnection(zf, ZmqEndpoint('connect', ip))
        names = locals()
        names['client-%s' % i] = Client(s)
        c_list.append(names['client-%s' % i])
    return c_list


def test():
    start = time.time()
    print('begin: ', start)
    for c in generate_c():
        c.request()
    end = time.time()
    print('end: ', end)
    print('total time: %s' % (end-start))

reactor.callWhenRunning(test)
reactor.run()