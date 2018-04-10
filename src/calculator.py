from file_loader import Analyzer
import re

input_path = '../data/input.txt'
output_path = '../data/output.txt'

class Calculator:
    def __init__(self):
        self.word = []
        self.pinyin = []
    def read_in(self, path):
        with open (path, 'r') as f:
            for line in f.readlines():
                cur_str = re.sub('\n', '', line)
                self.pinyin.append(re.split(' ', cur_str))
    def calculate(self, analyzer):
        for py_list in self.pinyin:
            cur_word = '' 
            for py in py_list:
                for item in analyzer.find_choice(py,1,1):
                    cur_word = cur_word + item[0]
            print(cur_word)
            self.word.append(cur_word)
        pass


a = Analyzer()
c = Calculator()
a.load()
for item in a.find_choice('bei jing', 2, 2):
    print(item[0] + str(item[1]))
c.read_in(input_path)
c.calculate(a)

