# coding: utf-8
"""override the context ---> MAX_SOCKETS---> 10000"""


from zmq import Context as ContextBase

# notice when exiting, to avoid triggering term on exit


class Context(ContextBase):
    """Create a zmq Context

    A zmq Context creates sockets via its ``ctx.socket`` method.
    """
    sockopts = None

    def __init__(self):
        super(Context, self).__init__()
        self.MAX_SOCKETS = 100000
        self.SNDHWM = 100000
        # self.sockopts = {'MAX_SOCKETS': 10000}
        # self.setsockopt('MAX_SOCKETS', 10000)
        # print('MAX_SOCKETS: ', self.getsockopt('MAX_SOCKETS'))

