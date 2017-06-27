import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
# socket.bind("tcp://*:5555")


def do_foo():  
    print "foo!"  
  
def do_bar():  
    print "bar!"  
  
class Print():  
    def do_foo(self):  
        print "foo!"  
  
    def do_bar(self):  
        print "bar!"  
 
    @staticmethod  
    def static_foo():  
        print "static foo!"  
 
    @staticmethod  
    def static_bar():  
        print "static bar!"  
  
def main():  
    obj = Print()  
  
    func_name = "do_foo"  
    static_name = "static_foo"  
    eval(func_name)()  
    getattr(obj, func_name)()  
    getattr(obj, static_name)()  
  
    func_name = "do_bar"  
    static_name = "static_bar"  
    eval(func_name)()  
    getattr(obj, func_name)()  
    getattr(Print, static_name)()  
  
if __name__ == '__main__':  
    main()  


# while True:
#     #  Wait for next request from client
#     message = socket.recv()
#     print("Received request: %s" % message)

#     #  Do some 'work'
#     time.sleep(1)

#     #  Send reply back to client
#     socket.send(b"World")