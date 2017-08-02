from pypinyin import pinyin, lazy_pinyin, TONE2
import pypinyin
import csv
import codecs
from collections import OrderedDict
import json

def save_pinyin():
    py_words = {}
    n = []
    with open('chinese_simplified.txt', 'r') as f:
        lines = f.readlines()
        num = len(lines)
        for line in lines:
            num -= 1
            print('remain: %s' % num)
            print(line)
            line = line.strip()
            pys = set()
            for dyz in pinyin(line, style=TONE2)[0]:  # heteronym=True,
                py = ''.join(list(filter(str.isalpha, dyz)))
                pys.add(py)
            print(pys)
            for py in pys:
                if py in py_words.keys():
                    py_words[py].append(line)
                else:
                    py_words[py] = [line]
    return py_words
    # f = codecs.open('pinyin2.csv', 'w+', encoding='utf_8_sig')  # wb
    # # f.write(codecs.BOM_UTF8)   # in py2.7
    # writer = csv.writer(f)

    # for k, v in py_words.items():
    #     s = ''
    #     for word in v:
    #         s += word + ' '
    #     writer.writerow([k, s, len(v)])
    # f.close()


def sum(dic):
        s = 0
        for k, v in dic.items():
            s += len(v)
        return s

if __name__ == '__main__':
    # save_pinyin()
    special = ['sh', 'ch', 'zh']
    pinyin_dic = {}
    py_words = {}
    with open('pinyin.csv', 'r') as f:
        reader = csv.reader(f, dialect='excel')
        for py in reader:
            print(py[1])   # hanzi
            py_words[py[0]] = [x for x in py[1] if x != ' ']
            print(list(py[1]))
            py = py[0]  # pinyin
            py_2 = py[:2]
            if py_2 in special:  # sh
                if py_2 in pinyin_dic.keys():
                    pinyin_dic[py_2].append(py[2:])
                else:
                    pinyin_dic[py_2] = [py[2:]]
            else:
                if py[:1] in pinyin_dic.keys():
                    if py[1:] != '':
                        pinyin_dic[py[:1]].append(py[1:])
                else:
                    if py[1:] != '':
                        pinyin_dic[py[:1]] = [py[1:]]
    # print(len(pinyin_dic))
    # f = codecs.open('pinyin3.csv', 'w+', encoding='utf_8_sig')  # wb
    # writer = csv.writer(f)
    #
    # for k, v in pinyin_dic.items():
    #     s = ''
    #     for word in v:
    #         s += word + ' '
    #     writer.writerow([k, s])
    # f.close()
    bigdic = {}

    for k, v in pinyin_dic.items():
        innerdic = {}
        innerkeys = []
        for i in v:
            innerkeys.append(k+i)
        for key in innerkeys:

            innerdic[key] = py_words[key]

        bigdic[k] = OrderedDict(sorted(innerdic.items(),
                                       key=lambda x: len(x[1]), reverse=True))

    bd = sorted(bigdic.items(), key=lambda x: sum(x[1]), reverse=True)
    print(json.dumps(OrderedDict(bd), ensure_ascii=False))




# >>> import re
# >>> non_decimal = re.compile(r'[^\d.]+')
# >>> non_decimal.sub('', '12.3fe5e')
# '12.35

