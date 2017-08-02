import json
from collections import OrderedDict

word_dic = dict()
print(type(word_dic))
with open('english.txt', 'r') as f:
    lines = f.readlines()
    num = len(lines)

    for word in lines:
        num -= 1
        print('remain: %s' % num)
        print(word)
        word = word.strip()
        word_len = len(word)
        print(type(word_dic))
        if word_len in word_dic.keys():
            word_dic[word_len].append(word)
        else:
            word_dic[word_len] = [word]
    word_dic = sorted(word_dic.items(), key=lambda x: x[0], reverse=True)
    print(json.dumps(OrderedDict(word_dic), ensure_ascii=False))
