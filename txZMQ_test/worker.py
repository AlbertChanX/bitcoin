# coding:utf-8
from txzmq import ZmqEndpoint, ZmqFactory, ZmqPubConnection, ZmqRouterConnection, ZmqREPConnection, ZmqDealerConnection
from twisted.internet import reactor
import uuid

zf = ZmqFactory()

backend = ZmqEndpoint('bind', 'tcp://127.0.0.1:8880')  # dealer
# frontend = ZmqEndpoint('bind', 'tcp://127.0.0.1:8881')    # router
pub = ZmqEndpoint('bind', 'tcp://127.0.0.1:8881')


recv = ZmqREPConnection(zf, backend)  # REP
send = ZmqPubConnection(zf, pub)      # Pub


def b2str(id):
    # print uuid.UUID(bytes=id)
    return str(uuid.UUID(bytes=id))


# ZmqREPConnection
def doPrint(messageId, message):  # uuid
    print "Replying to %s, %r" % (b2str(messageId), message)
    recv.reply(messageId, "%s %r " % (b2str(messageId), message))  # reply to client (id+msg) by mId
    # pub ---> 8881
    send.publish(message, tag='btc')

recv.gotMessage = doPrint
reactor.run()







