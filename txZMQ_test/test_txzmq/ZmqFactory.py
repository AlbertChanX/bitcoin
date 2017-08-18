"""
Override the zmqfactory
"""
from context import Context
from txzmq import ZmqFactory as zf


class ZmqFactory(zf):
    ioThreads = 1

    def __init__(self):
        """
        Constructor.

        Create ZeroMQ context.
        """
        self.connections = set()
        self.context = Context(self.ioThreads)

