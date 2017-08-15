# coding:utf-8
from txzmq import ZmqEndpoint, ZmqREQConnection, ZmqRequestTimeoutError
from twisted.internet import reactor
import time
import zmq
from ZmqFactory import ZmqFactory
import json

ip = 'tcp://10.10.0.233:8880'
s_ip = 'tcp://10.10.0.233:10000'
zf = ZmqFactory()
s = ZmqREQConnection(zf, ZmqEndpoint('connect', ip))
num = 0
sdata = {}
with open('block.json', 'r') as f:
    data = f.read()
    data = json.dumps(data) 
    sdata['data'] = data

class Client(object):
    def __init__(self,s,name):
        self.s = s
        self.name = name
        
    def request(self):
        def produce():
            print("Requesting  from %s" % (self.name))

            try:
                global num
                num += 1 
                print('the num of request: %d' %num)
                global sdata
                sdata['time'] = time.time()
                sdata['name'] = self.name
                print('%.6f' %sdata['time'])
                d = self.s.sendMsg(json.dumps(sdata), timeout=60*5)
                
                def doPrint(reply):  # else reply -->list
                    print("Got reply: %s" % (reply[0]))  # ???

                def onTimeout(fail):  # except
                    fail.trap(ZmqRequestTimeoutError)
                    print("Timeout on request, is reply server running?")
                    print('switching to other worker: %s' % s_ip)
                    
                    self.s.shutdown()
                    self.s = ZmqREQConnection(zf, ZmqEndpoint('connect', s_ip))
                d.addCallback(doPrint).addErrback(onTimeout)
            except zmq.error.Again:
                print("Skipping, no consumers...")
            #reactor.callLater(20, produce)
        reactor.callWhenRunning(produce)


def generate_c():
    c_list = []
    for i in range(1000):
        print(i)
        global s
        s = ZmqREQConnection(zf, ZmqEndpoint('connect', ip))
        names = locals()
        name = 'client-%s' % (i+1)
        names[name] = Client(s, name)
        c_list.append(names[name])
    return c_list


def test():
    start = time.time()
    print('begin: ', start)
    for c in generate_c():
       #print(getattr())
       c.request()
    end = time.time()
    print('end: ', end)
    print('total time: %s' % (end-start))

reactor.callWhenRunning(test)
reactor.run()
