# coding:utf-8
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPubConnection, ZmqRouterConnection, ZmqREPConnection, ZmqDealerConnection
import zmq
import time
from twisted.internet import reactor


zf = ZmqFactory()

backend = ZmqEndpoint('bind', 'tcp://127.0.0.1:8880')  # dealer
# frontend = ZmqEndpoint('bind', 'tcp://127.0.0.1:8881')    # router
pub = ZmqEndpoint('bind', 'tcp://127.0.0.1:8881')


recv = ZmqREPConnection(zf, backend)  # REP
send = ZmqPubConnection(zf, pub)      # Pub


# ZmqREPConnection
def doPrint(messageId, message):  # uuid
    print "Replying to %s, %r" % (messageId, message)
    recv.reply(messageId, "%s %r " % (messageId, message)) # reply to client by mId
    # pub ---> 8881
    send.publish(message, tag='btc')

recv.gotMessage = doPrint
reactor.run()







