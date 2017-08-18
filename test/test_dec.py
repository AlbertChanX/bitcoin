# coding:utf-8
import sys

# sys
def a():
    print(sys._getframe().f_code.co_name)
a()

# 使用修饰器就可以对函数指向一个变量，然后取变量对象的__name__方法


def timeit(func):
    def run(*argv):
       print(func.__name__)
       if argv:
        ret = func(*argv)
       else:
        ret = func()
       return ret
    return run


@timeit
def test(a):
    print a
test(1)

#   multi-inherit


class A(object):
    def __init__(self):
        print('This is init function of A')


class D(object):
    def __init__(self):
        print("I'm in D")


class B(object):
    def __init__(self):
        print('This is init function of B')
        super(B, self).__init__()    # call A's init()
        print('leaving B')


# B中使用了super()它就会遍历MRO，寻找下一个方法，在A中找到了，所以就调用了它

# 默认call第一个Class的init
class C(B, A):   # A, B 互换位置？--> only CALL A's init
    def __init__(self):
        print("I'm in C")
        super(C, self).__init__()   # == B.__init__(self)
        print('leaving C')

c = C()