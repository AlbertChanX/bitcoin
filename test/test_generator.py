# coding:utf-8

mygenerator = (x*x for x in range(3))  # () generator
print(type(mygenerator))
for i in mygenerator:
    print(i)


def createGenerator():
    mylist = range(3)
    for i in mylist:
        yield i*i

# 调用函数的时候,函数里的代码并没有运行.函数仅仅返回生成器对象
mygenerator = createGenerator()  # 创建生成器
print(mygenerator)  # mygenerator is an object!

for i in mygenerator:
    print(i)
s = 'i am string'
print(type(s))
b = str.encode(s)
print(type(b))   # in py3  class 'bytes'
c = s.encode()   # in py3  class 'bytes'
print(type(c))

original_unicode_str = u'hello world'
utf8_str = original_unicode_str.encode("utf-8")
print('is unicode=',isinstance(original_unicode_str, unicode)) # True
print("uft-8 is unicode=",isinstance(utf8_str, unicode) )# False
print("is str=",isinstance(original_unicode_str, str) )# False
print("uft-8 is str=",isinstance(utf8_str, str) )# True
print("unicode str size=", len(original_unicode_str) )# 6703
print("utf8 str size =",len(utf8_str)) # 7489