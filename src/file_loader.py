#! python3
# -*- coding=utf8 -*-

'''
使用Python3较好地支持unicode
'''

import json
import re
from pypinyin import pinyin, lazy_pinyin

src_file = '../../sina_news/2016-01.txt'
test_file = '../../sina_news/test.txt'
output_file = '../data/output.txt'

class Analyzer:
    def __init__(self):
        self.content = []
        self.data_base = {} 
        self.total_num = 0
    def load_data(self):
        re_exp = " |，|。|？|：|；|、|（|）|\d*|[a-z]*|[A-Z]*|\/"
        with open(test_file, 'r') as f:
            for line in f.readlines():
                lineData = json.loads(line)
                data = lineData.get('html')
                title = lineData.get('title')
                for s in re.split(re_exp, data):
                    self.content.append(s)
                '''
                print('Finish--'+title)
                '''
    def analyze(self):
        for item in self.content:
            for i in range(0, len(item)-2):
                x = item[i:i+2]
                xpy = lazy_pinyin(x)
                x_pinyin = xpy[0] + ' ' + xpy[1] 
                if x_pinyin not in self.data_base:
                    self.data_base[x_pinyin] = {} 
                    self.data_base[x_pinyin][x] = 1
                else:
                    if x not in self.data_base[x_pinyin]:
                        self.data_base[x_pinyin][x] = 1
                    else:
                        self.data_base[x_pinyin][x] = self.data_base[x_pinyin][x] + 1 
                self.total_num = self.total_num + 1
    def write_result(self):
        with open (output_file, 'w') as f:
            '''
            f.write(json.dumps(self.data_base))
            '''
            for k in self.data_base.keys():
                result = {}
                result['Pinyin'] = k
                result['Word'] = {}
                for word in self.data_base[k].keys():
                    result['Word'][word] = self.data_base[k][word]
                print(result)
                f.write(json.dumps(result)+'\n')
    def load_result(self):
        with open(output_file, 'r') as f:
            for line in f.readlines():
                lineData = json.loads(line)
        

loader = Analyzer()
loader.load_data()
loader.analyze()
loader.write_result()
loader.load_result()
