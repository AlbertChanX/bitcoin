# coding: utf-8
"""override the context ---> MAX_SOCKETS---> 10000"""


from zmq import Context as ContextBase

# notice when exiting, to avoid triggering term on exit


class Context(ContextBase):
    """Create a zmq Context

    A zmq Context creates sockets via its ``ctx.socket`` method.
    """
    sockopts = None

    def __init__(self, io_threads=1, **kwargs):
        super(Context, self).__init__(io_threads=io_threads, **kwargs)
        self.MAX_SOCKETS = 10000
        # self.sockopts = {'MAX_SOCKETS': 10000}
        # self.setsockopt('MAX_SOCKETS', 10000)
        # print('MAX_SOCKETS: ', self.getsockopt('MAX_SOCKETS'))

