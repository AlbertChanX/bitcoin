# coding:utf-8
from twisted.internet.defer import inlineCallbacks, Deferred, returnValue
from twisted.python.failure import Failure
from time import time
from twisted.internet import reactor, defer


def loadRemoteData(callback):   # in defer.py def callback(self, result):
    import time
    time.sleep(2)
    callback(1)


def loadRemoteData2(callback):
    import time
    time.sleep(1)
    callback(2)


@defer.inlineCallbacks
def getRemoteData():
    d1 = defer.Deferred()  # deferred task 1
    reactor.callInThread(loadRemoteData, d1.callback)  # d1.callback --> loadRemoteData
    r1 = yield d1

    d2 = defer.Deferred()  # deferred task 2
    reactor.callInThread(loadRemoteData2, d2.callback)
    r2 = yield d2

    returnValue(r1 + r2)


def getResult(v):   # callback method
    print "result=", v
    print('end_time: %s' % time())


if __name__ == '__main__':
    print('start_time: %s' % time())
    d = getRemoteData()    # big deferred task
    d.addCallback(getResult)   # callback方法传入的参数就是Defered的结果
    reactor.callLater(5, reactor.stop)
    reactor.run()