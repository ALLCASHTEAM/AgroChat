import pandas as pd

def convert(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read().count('\n')
    with open(filename, 'r', encoding='utf-8') as k:
        for i in range(c):

            data = k.readline().replace('\n', ' ').split(' - ')
            print(data)


if __name__ == '__main__':
    convert('qaByGPTWithOutDots.txt')