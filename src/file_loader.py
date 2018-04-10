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
pinyin_lib = '../data/一二级汉字表.txt'
single_file = '../data/single_word.txt'
double_file = '../data/double_word.txt'
triple_file = '../data/triple_word.txt'
cnt_file = '../data/cnt.txt'

class Analyzer:
    def __init__(self):
        self.content = []
        self.double_db = {} 
        self.single_db = {}
        self.triple_db = {}
        self.single_num = 0
        self.double_num = 0
        self.triple_num = 0
    def load_data(self):
        '''将汉字之外的符号与字母用正则表达式过滤'''
        re_exp = '[^\u4e00-\u9fff]+'
        with open(test_file, 'r') as f:
            for line in f.readlines():
                lineData = json.loads(line)
                data = lineData.get('html')
                title = lineData.get('title')
                for s in re.split(re_exp, data):
                    self.content.append(s)
        '''Todo...输入一二级汉字表'''
    def analyze(self):
        for item in self.content:
            l = len(item)
            for i in range(0, l):
                ''' 单个字出现统计 '''
                letter = item[i]
                l_pinyin = lazy_pinyin(letter)[0]
                if l_pinyin not in self.single_db:
                    self.single_db[l_pinyin] = {}
                    self.single_db[l_pinyin][letter] = 1
                else:
                    if letter not in self.single_db[l_pinyin]:
                        self.single_db[l_pinyin][letter] = 1
                    else:
                        self.single_db[l_pinyin][letter] = self.single_db[l_pinyin][letter] + 1
                self.single_num = self.single_num + 1
                ''' 二元组出现次数统计 '''
                if i < l-2:
                    x = item[i:i+2]
                    xpy = lazy_pinyin(x)
                    x_pinyin = xpy[0] + ' ' + xpy[1] 
                    if x_pinyin not in self.double_db:
                        self.double_db[x_pinyin] = {} 
                        self.double_db[x_pinyin][x] = 1
                    else:
                        if x not in self.double_db[x_pinyin]:
                            self.double_db[x_pinyin][x] = 1
                        else:
                            self.double_db[x_pinyin][x] = self.double_db[x_pinyin][x] + 1 
                    self.double_num = self.double_num + 1
                ''' 三元组出现次数统计 '''
                if i < l-3:
                    tri = item[i:i+3]
                    tri_py = lazy_pinyin(tri)
                    tri_pinyin = tri_py[0] + ' ' + tri_py[1] + ' ' + tri_py[2] 
                    if tri_pinyin not in self.triple_db:
                        self.triple_db[tri_pinyin] = {} 
                        self.triple_db[tri_pinyin][tri] = 1
                    else:
                        if tri not in self.triple_db[tri_pinyin]:
                            self.triple_db[tri_pinyin][tri] = 1
                        else:
                            self.triple_db[tri_pinyin][tri] = self.triple_db[tri_pinyin][tri] + 1 
                    self.triple_num = self.triple_num + 1
    def write_result(self, file_path, database):
        with open (file_path, 'w') as f:
            for k in database.keys():
                result = {}
                result['Pinyin'] = k
                result['Word'] = {}
                for word in database[k].keys():
                    result['Word'][word] = database[k][word]
                f.write(json.dumps(result)+'\n')
    def load_result(self, file_path, database):
        with open(file_path, 'r') as f:
            for line in f.readlines():
                lineData = json.loads(line)
                py = lineData['Pinyin']
                if py not in database.keys():
                    database[py] = {}
                for words in lineData['Word'].keys():
                    database[py][words] = lineData['Word'][words]
    def write_cnt(self):
        with open(cnt_file, 'w') as f:
            cnt_result = {}
            cnt_result['Single'] = self.single_num
            cnt_result['Double'] = self.double_num
            cnt_result['Triple'] = self.triple_num
            f.write(json.dumps(cnt_result))
    def load_cnt(self):
        with open(cnt_file, 'r') as f:
            data = json.loads(f.readline())
            self.single_num = data.get('Single')
            self.double_num = data.get('Double')
            self.triple_num = data.get('Triple')
    def dict_sort(self, py, choice_num, database):
        if py not in database.keys():
            return ['x']
        dict_size = len(database[py])
        result = sorted(database[py].items(), key=lambda e:e[1],reverse = True)
        if dict_size < choice_num:
            return result 
        return result[0:choice_num]
    def find_choice(self, py, lth, choice_num):
        if lth == 2:
            return self.dict_sort(py,choice_num,self.double_db)
        elif lth == 3:
            return self.dict_sort(py,choice_num,self.double_db)
        else:
            return self.dict_sort(py,choice_num,self.single_db)
    def show_db(self):
        print(self.single_db)
        print(self.double_db)
        print(self.triple_db)
    def load(self):
        self.load_result(single_file, self.single_db)
        self.load_result(double_file, self.double_db)
        self.load_result(triple_file, self.triple_db)



'''
loader = Analyzer()
loader.load_data()
loader.analyze()
loader.write_cnt()
loader.write_result(single_file, loader.single_db)
loader.write_result(double_file, loader.double_db)
loader.write_result(triple_file, loader.triple_db)
loader.load_result(single_file, loader.single_db)
loader.load_result(double_file, loader.double_db)
loader.load_result(triple_file, loader.triple_db)
loader.load_cnt()
loader.load()
loader.show_db()
'''
