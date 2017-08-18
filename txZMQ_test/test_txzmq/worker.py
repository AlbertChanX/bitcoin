# coding:utf-8
from txzmq import ZmqEndpoint, ZmqPubConnection, ZmqRouterConnection, ZmqREPConnection, ZmqDealerConnection
from twisted.internet import reactor
import uuid
import json,time
from ZmqFactory import ZmqFactory
from optparse import OptionParser
"""
cpu, the number of client, 
"""
"""
Example txzmq worker.

    python worker.py  --ep1=tcp://127.0.0.1:8880 --ep2=tcp://127.0.0.1:8881

    python worker.py  --ep1=tcp://10.10.0.233:10000 --ep2=tcp://10.10.0.233:10001

"""
# default settings
ip1 = 'tcp://10.10.0.233:8880'
ip2 = 'tcp://10.10.0.233:8881'
def b2str(id):
    # print uuid.UUID(bytes=id)
    return str(uuid.UUID(bytes=id))

parser = OptionParser("")
parser.add_option("-p", "--ep1", dest="ep1", help="like tcp://127.0.0.1:8880")
parser.add_option("-e", "--ep2", dest="ep2", help="like tcp://127.0.0.1:8880")
parser.set_defaults(ep1=ip1, ep2=ip2)

(options, args) = parser.parse_args()

zf = ZmqFactory()

backend = ZmqEndpoint('bind', options.ep1)  # dealer
# frontend = ZmqEndpoint('bind', 'tcp://127.0.0.1:8881')    # router
pub = ZmqEndpoint('bind', options.ep2)

recv = ZmqREPConnection(zf, backend)  # REP
send = ZmqPubConnection(zf, pub)      # Pub

num = 0
# ZmqREPConnection


def doPrint(messageId, message):  # uuid
    # if time.time() - 6.0 <= float(message):
        # print(message[0])
        data = json.loads(message)
        # print(type(data['name'].encode()))
        print("Replying to %s, %r time is %s" % (b2str(messageId), data['name'], data['time']))
        recv.reply(messageId, "%s reply to: %s" % (b2str(messageId), data['name'].encode('utf-8')))  # reply to client (id+msg) by mId
    # pub ---> 8881
        # print(message)
        global num
        num += 1
        # print(type(message))
        send.publish(message, tag=data['name'].encode()+'btc')
        print('the publish num is %s now is %s' %(num,time.time()))

recv.gotMessage = doPrint
reactor.run()






