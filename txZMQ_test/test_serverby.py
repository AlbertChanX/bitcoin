# coding:utf-8
from txzmq import ZmqEndpoint, ZmqREQConnection, ZmqRequestTimeoutError
from twisted.internet import reactor
import time
import zmq
from ZmqFactory import ZmqFactory
import json

ip = 'tcp://127.0.0.1:8880'
zf = ZmqFactory()
s = ZmqREQConnection(zf, ZmqEndpoint('connect', ip))
num = 0
senddata = {}
with open('block.json', 'r') as f:
    data = f.read()
    data = json.dumps(data)  # .encode('utf-8')
    senddata['data'] = data

class Client(object):
    def __init__(self, s):
        self.s = s

    def request(self):
        def produce():
            # j_data = dict()
            now = str(time.time())
            # print(len(now.encode('utf-8')))
            # j_data['time'] = now


            # print(data)
            # print("Requesting %r" % data)
            # print(json.loads(data)['time'])
            try:
                global num
                num += 1
                print('the num of request: %d, time is %s' % (num, now))
                global senddata
                senddata['time'] = now
                senddata['channel'] = num
                d = self.s.sendMsg(json.dumps(senddata), timeout=60)

                def doPrint(reply):  # else reply -->list
                    print("Got reply: %s" % (reply[0]))  # ???

                def onTimeout(fail):  # except
                    fail.trap(ZmqRequestTimeoutError)
                    print("Timeout on request, is reply server running?")
                    self.s.shutdown()
                    self.s = ZmqREQConnection(zf, ZmqEndpoint('connect', ip))
                d.addCallback(doPrint).addErrback(onTimeout)
            except zmq.error.Again:
                print("Skipping, no consumers...")
            # reactor.callLater(10, produce)
        reactor.callWhenRunning(produce)


def generate_c():
    c_list = []
    for i in range(1000):
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