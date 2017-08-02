# coding:utf-8

import pyttsx

engine = pyttsx.init()
engine.say('hello world')
engine.say('hi')
engine.runAndWait()
# 朗读一次
engine.endLoop()
print('ok')