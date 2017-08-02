# coding:utf-8
import pyttsx

engine = pyttsx.init()
engine.say('hello Sally')
engine.say('你好')
engine.runAndWait()
# 朗读一次
engine.endLoop()
print('ok')
