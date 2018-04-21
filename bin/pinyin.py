import sys, getopt
sys.path.append('../src')
from file_loader import Analyzer
from calculator import Calculator

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 2:
        print('Please input as: python3 pinyin.py ../data/input.txt ../data/output.txt')
        print('Or test with: python3 pinyin.py ../data/test_1.txt')
    else:
        a = Analyzer()
        a.load()
        c = Calculator(a)
        if len(sys.argv) == 3:
            ipt_path = sys.argv[1]
            opt_path = sys.argv[2]
            c.solve(ipt_path, opt_path)
        elif len(sys.argv) == 2:
            test_path = sys.argv[1]
            c.test(test_path)
