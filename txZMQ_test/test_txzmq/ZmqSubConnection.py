
from zmq import constants

from txzmq import ZmqSubConnection as zsc
import time,json
num = 0
class ZmqSubConnection(zsc):

    def gotMessage(self, message, tag):
        """
        Called on incoming message recevied by subscriber.

        Should be overridden to handle incoming messages.

        :param message: message data
        :param tag: message tag
        """
        global num
        num += 1
        data = json.loads(message)
        now = time.time()
        print('%.6f' %now)
        print('%.6f' %data['time'])
        interval = now - data['time']
        print('the num is %d \nI am %s subscribe %s, received %s %s now is %s interval is:%.6f' % (num, self.name, tag, data['time'], data['name'], now, interval))

