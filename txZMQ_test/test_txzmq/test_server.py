# coding:utf-8

from txzmq import ZmqEndpoint 
from ZmqSubConnection import ZmqSubConnection
from twisted.internet import reactor
from ZmqFactory import ZmqFactory
import time
import json
ip = 'tcp://10.10.0.233:8881'
ip_s = 'tcp://10.10.0.233:10001'
zf = ZmqFactory()
#global sub
sub = ZmqSubConnection(zf, ZmqEndpoint('connect', ip))
#sub.subscribe("btc")


class Server(object):
      def __init__(self, sub, sub2):
          self.sub = sub
          self.sub2 = sub2

def doPrint(*args):  # gotMessage(self, message, tag):
    global num
    num += 1
    print("the num of data: %d" % (num))
    print('interval is %s', json.loads(args[0])['time'])
    print "I'm , message received: %r" % (args,)


def generate_s():
    for i in range(1000):
        s_list = []
        global sub, sub2
        sub = ZmqSubConnection(zf, ZmqEndpoint('connect', ip))
        sub2 = ZmqSubConnection(zf, ZmqEndpoint('connect', ip_s))
        channel = 'client-%sbtc' %(i+1)
        print('channel:%s ' % channel)
        sub.subscribe(channel)
        sub2.subscribe(channel)
        #sub.subscribe('client-2btc')
        #sub.gotMessage = doPrint
        name = 'server-%s' %(i+1)
        sub.name = name
        sub2.name = 'server-%s:10001'
        names = dict()
        names[name] = Server(sub,sub2)
 


def test():
    start = time.time()
    print('begin: ', start)
    for s in generate_s():
        s.getmsg()
    end = time.time()
    print('end: ', end)
    print('total time: %s' % (end-start))

if __name__ == "__main__":
    generate_s()
    reactor.run()

