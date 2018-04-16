from file_loader import Analyzer
import re
from pypinyin import lazy_pinyin
import math
import sys

input_path = '../data/input的副本.txt'
output_path = '../data/output.txt'
test_path = '../data/test.txt'
c_num = 20
alpha = 0.01 
beta = 1 - alpha
min_num = -100000

class node:
    def __init__(self):
        self.s = '' 
        self.f = 0.0

class Calculator:
    def __init__(self,a):
        self.analyzer = a
        self.pb_dict = {} 
        self.pinyin = []
        self.ans_sentence = {}
        self.ans_dict = {}
        self.ans = []
        self.word_cnt = 0
        self.stc_cnt = 0
    def read_in(self, path):
        with open (path, 'r') as f:
            for line in f.readlines():
                cur_str = re.sub('\n', '', line)
                self.pinyin.append(re.split(' ', cur_str))
    def read_test(self, path):
        with open(path, 'r') as f:
            l = 0
            for line in f.readlines():
                cur_str = re.sub('\n', '', line)
                if l == 0:
                    self.pinyin.append(re.split(' ', cur_str))
                    l = 1
                elif l == 1:
                    cur_stc = re.sub(' ', '', cur_str)
                    self.ans.append(cur_stc)
                    l = 0
    def cmp_stc(self, str_1, str_2):
        self.stc_cnt = self.stc_cnt + 1 
        if str_1 == str_2:
            return True
        return False
    def cmp_word(self, str_1, str_2):
        l = min(len(str_2), len(str_1))
        self.word_cnt = self.word_cnt + l
        cnt = 0
        for i in range(0,l):
            if str_1[i] == str_2[i]:
                cnt = cnt + 1
        return cnt
    def viterbi(self):
        k = 0
        stc_num = 0
        wd_num = 0
        for py_list in self.pinyin:
            ans_stc = ''
            l = len(py_list) - 1
            self.pb_dict = {} 
            self.ans_sentence = {}
            self.ans_dict = {}
            for i in range(1, l):
                py = py_list[i-1].lower() + ' ' + py_list[i].lower()
                cur_list = self.analyzer.find_choice(py_list[i].lower(), 1)
                last_list = self.analyzer.find_choice(py_list[i-1].lower(), 1)
                pair_list = self.analyzer.find_choice(py, 2)
                tmp_dict = {}
                max_f = min_num
                tmp_w = ''
                for cur in cur_list:
                    cur = cur[0]
                    tmp_dict[cur] = {}
                    for item in last_list:
                        last = item[0]
                        tmp_dict[cur][last] = min_num 
                        pair_cnt = self.sum(last+cur, pair_list) 
                        p = self.trans_pbty(last,cur,last_list,cur_list,pair_list)
                        if i == 1:
                            tmp_dict[cur][last] = p + math.log(item[1])-math.log(self.analyzer.single_num) 
                        else:
                            for j in self.pb_dict[i-1][last].keys():
                                f = self.pb_dict[i-1][last][j] + p 
                                if f > tmp_dict[cur][last]:
                                    tmp_dict[cur][last] = f
                        if tmp_dict[cur][last] > max_f:
                            max_f = tmp_dict[cur][last]
                            if i < l-1:
                                tmp_w = last
                            else:
                                tmp_w = last+cur
                ans_stc = ans_stc + tmp_w
                self.pb_dict[i] = tmp_dict
            '''
            p = min_num
            next_w = ''
            cur_w = ''
            for cur in self.pb_dict[l-1].keys():
                for item in self.pb_dict[l-1][cur].keys():
                    if self.pb_dict[l-1][cur][item] > p:
                        p = self.pb_dict[l-1][cur][item]
                        cur_w = cur
                        next_w = item 
            print(cur_w + next_w)
            ans_st = self.find_ans_1(l-2, next_w) + cur_w

            ans_list = []
            self.ans_dict = {}
            for cur in self.pb_dict[l-1].keys():
                ans_list.append(self.find_ans(l-1, cur))
            ans_nd = node()
            ans_nd.f = min_num 
            for item in ans_list:
                if item.f > ans_nd.f:
                    ans_nd = item
            '''
            if self.cmp_stc(ans_stc, self.ans[k]):
                #print('correct: ' + ans_nd.s)
                print('correct: ' + ans_stc)
                stc_num = stc_num + 1
            else:
                #print('wrong: ' + ans_nd.s + '/ ' + self.ans[k])
                print('wrong: ' + ans_stc + '/ ' + self.ans[k])
            wd_num = wd_num + self.cmp_word(ans_stc, self.ans[k])
            k = k + 1
        print('句子正确率：' + str(stc_num/self.stc_cnt))
        print('字正确率：' + str(wd_num/self.word_cnt))
    def find_ans(self, i, cur):
        if i not in self.ans_dict.keys():
            self.ans_dict[i] = {}
        if cur not in self.ans_dict[i].keys():
            nd = node()
            if i == 0:
                nd.f = 0.0
                nd.s = ''
            else:
                nd.f = min_num 
                for item in self.pb_dict[i][cur].keys():
                    n = self.find_ans(i-1,item)
                    p = self.pb_dict[i][cur][item] + n.f
                    if p > nd.f:
                        nd.f = p
                        if i == 1:
                            nd.s = item + cur
                        else:
                            nd.s = n.s + cur 
            self.ans_dict[i][cur] = nd
        #print(self.ans_dict[i][cur].s)
        return self.ans_dict[i][cur]
    def find_ans_1(self, i, cur):
        p = 0.0
        next_w = ''
        for item in self.pb_dict[i][cur].keys():
            if self.pb_dict[i][cur][item] > p:
                p = self.pb_dict[i][cur][item]
                next_w = item 
        return self.find_ans_1(i-1, next_w) + cur
    def sum(self, word, word_list):
        for item in word_list:
            if word == item[0]:
                if len(item) > 1:
                    return item[1]
        return 0
    def trans_pbty(self, last, cur, last_list, cur_list, pair_list):
        cur_cnt = self.sum(cur, cur_list)
        last_cnt = self.sum(last, last_list)
        pair_cnt = self.sum(last+cur, pair_list)
        if last_cnt == 0 or pair_cnt == 0:
            if cur_cnt == 0:
                return math.log(alpha)-math.log(self.analyzer.single_num)
            return math.log(alpha)+math.log(cur_cnt)-math.log(self.analyzer.single_num)
        else:
            return math.log(alpha*(cur_cnt/self.analyzer.single_num) + beta*(pair_cnt / last_cnt)) 
        
a = Analyzer()
a.load()
c = Calculator(a)
#c.read_in(input_path)
c.read_test(test_path)
c.viterbi()
