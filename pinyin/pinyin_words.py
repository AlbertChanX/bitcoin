from pypinyin import pinyin, lazy_pinyin, TONE2
import pypinyin
import csv
import codecs


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
                    # if num == 2000:
                    #     break
    f = codecs.open('pinyin2.csv', 'w+', encoding='utf_8_sig')  # wb
    # f.write(codecs.BOM_UTF8)   # in py2.7
    writer = csv.writer(f)

    for k, v in py_words.items():
        s = ''
        for word in v:
            s += word + ' '
        writer.writerow([k, s, len(v)])
    f.close()

if __name__ == '__main__':
    # save_pinyin()
    special = ['sh', 'ch', 'zh']
    pinyin = {}
    with open('pinyin2.csv', 'r') as f:
        reader = csv.reader(f, dialect='excel')
        for py in reader:
            print(py[1])

            py = py[0]

            py_2 = py[:2]
            if py_2 in special:  # sh
                if py_2 in pinyin.keys():
                    pinyin[py_2].append(py[2:])
                else:
                    pinyin[py_2] = [py[2:]]
            else:
                if py[:1] in pinyin.keys():
                    pinyin[py[:1]].append(py[1:])
                else:
                    pinyin[py[:1]] = [py[1:]]
    print(len(pinyin))
    # f = codecs.open('pinyin3.csv', 'w+', encoding='utf_8_sig')  # wb
    # writer = csv.writer(f)
    #
    # for k, v in pinyin.items():
    #     s = ''
    #     for word in v:
    #         s += word + ' '
    #     writer.writerow([k, s])
    # f.close()
    for k, v in pinyin.items():
        print(k, v)




# >>> import re
# >>> non_decimal = re.compile(r'[^\d.]+')
# >>> non_decimal.sub('', '12.3fe5e')
# '12.35

