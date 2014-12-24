from collections import Counter
from itertools import zip_longest
from os.path import splitext
from sys import argv, stdin, stderr
import re

import numpy as np

import ass
import pysrt

漢字 = '\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A'
無漢字 = re.compile('[^{}]'.format(漢字), re.UNICODE)

def 只漢字残(文):
    return re.sub(無漢字, '', 文)

def 字数漢字(本):
    字数 = Counter()
    for 文 in 本:
        字数.update(只漢字残(文))
    return 字数

def 字数漢字本(名):
    with open(名, 'r') as 本:
        return 字数漢字(本)

def 字数漢字本ass(名):
    with open(名, 'r') as 本:
        字幕 = (文.text for 文 in ass.parse(本).events)
        return 字数漢字(字幕)

def 字数漢字本srt(名):
    字幕 = pysrt.open(名)
    字幕 = (文.text for 文 in 字幕)
    return 字数漢字(字幕)

def 字数漢字本店(名):
    尾 = splitext(名)[1]
    if 尾 == '.srt':
        return 字数漢字本srt(名)
    elif 尾 == '.ass':
        return 字数漢字本ass(名)
    else:
        return 字数漢字本(名)

def 字数漢字森(多名):
    字数 = Counter()
    if 多名 is stdin:
        字数 += 字数漢字(多名)
    else:
        for 名 in 多名:
            try:
                字数 += 字数漢字本店(名)
            except Exception as e:
                print(e, file=stderr)
                pass
    return 字数

if __name__ == '__main__':
    名 = stdin
    if len(argv) > 1:
        名 = argv[1:]

    字数 = 字数漢字森(名)
    全 = sum(字数.values())
    増 = np.cumsum([数 for _, 数 in 字数.most_common()])
    for 回, ((字, 数)), 加 in zip(range(len(字数)), 字数.most_common(), 増):
        print(回, 字, '{:.2%}'.format(数/全), '{:.2%}'.format(加/全))
