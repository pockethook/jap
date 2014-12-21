import re
from sys import argv
from collections import Counter

漢字 = '\u3400-\u4DB5\u4E00-\u9FCB\uF900-\uFA6A'
只漢字 = re.compile('[{}]'.format(漢字), re.UNICODE)
無漢字 = re.compile('[^{}]'.format(漢字), re.UNICODE)

def 只漢字残(一):
    return re.sub(無漢字, '', 一.decode())

def 無漢字残(一):
    return re.sub(只漢字, '', 一.decode())

def 字数漢字(本):
    字数 = Counter()
    for 一 in 本:
        字数 += Counter(只漢字残(一))
    return 字数.most_common()


if __name__ == '__main__':
    with open(argv[1], 'rb') as 本:
        字数 = 字数漢字(本)
        for 字, 数 in reversed(字数):
            print(字, 数)
        print(len(字数))
