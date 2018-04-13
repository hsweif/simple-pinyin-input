from file_loader import Analyzer
import re
from pypinyin import lazy_pinyin
import math

input_path = '../data/input.txt'
output_path = '../data/output.txt'
c_num = 20
alpha = 0.0000000000000001
beta = 1

class Calculator:
    def __init__(self,a):
        self.word = []
        self.pinyin = []
        self.analyzer = a
    def read_in(self, path):
        with open (path, 'r') as f:
            for line in f.readlines():
                cur_str = re.sub('\n', '', line)
                self.pinyin.append(re.split(' ', cur_str))
    def viterbi(self):
        for py_list in self.pinyin:
            l = len(py_list)
            pbty_arr = {} 
            for i in range(1, l):
                py = py_list[i-1] + ' ' + py_list[i]
                cur_list = self.analyzer.find_choice(py_list[i], 1)
                last_list = self.analyzer.find_choice(py_list[i-1], 1)
                pair_list = self.analyzer.find_choice(py, 2)
                tmp_dict = {}
                for cur in cur_list:
                    cur = cur[0]
                    tmp_dict[cur] = {}
                    for last in last_list:
                        last = last[0]
                        tmp_dict[cur][last] = 0.0
                        pair_cnt = self.sum(last+cur, pair_list) 
                        p = self.trans_pbty(last,cur,last_list,cur_list,pair_list)
                        if i == 1:
                            tmp_dict[cur][last] = p
                        else:
                            for j in pbty_arr[i-1][last].keys():
                                f = pbty_arr[i-1][last][j] * p 
                                if f > tmp_dict[cur][last]:
                                    tmp_dict[cur][last] = f
                pbty_arr[i] = tmp_dict
            k = l-1
            ans_st = ''
            next_w = ''
            while k > 0:
                f = 0.0
                for cur in pbty_arr[k].keys():
                    for last in pbty_arr[k][cur].keys():
                        if pbty_arr[k][cur][last] > f:
                            f = pbty_arr[k][cur][last]
                            cur_w = cur
                            next_w = last
                ans_st = cur_w + ans_st
                k = k-1
            ans_st = next_w + ans_st
            print(ans_st)
    def sum(self, word, word_list):
        for item in word_list:
            if word == item[0]:
                return item[1]
        return 0
    def trans_pbty(self, last, cur, last_list, cur_list, pair_list):
        '''not finished'''
        cur_cnt = self.sum(cur, cur_list)
        last_cnt = self.sum(last, last_list)
        pair_cnt = self.sum(last+cur, pair_list)
        if last_cnt == 0 or pair_cnt == 0:
            return alpha*cur_cnt/self.analyzer.single_num
        else:
            return alpha*(cur_cnt/self.analyzer.single_num) + beta*(pair_cnt / last_cnt) 
        
a = Analyzer()
a.load()
c = Calculator(a)
c.read_in(input_path)
c.viterbi()

