# -*- coding:utf-8 -*-
import random

'''
Криптографические тесты (NIST)
'''

class Frequency():
    n0 = 0
    n1 = 0
    n_all = 0
    fr_map = {}

    def Init(self, data):
        self.n0, self.n1 = 0, 0
        self.fr_map = dict(zip([i for i in range(256)], [0 for i in range(256)]))
        for s in data:
            self.n_all += 8
            self.fr_map[s] += 1
            bin_char = '0' * (8 - len(bin(s)[2::])) + bin(s)[2::]
            for i in bin_char:
                if i == '1':
                    self.n1 += 1
                else:
                    self.n0 += 1
        return 0

class Entropy_test():
    def wait(self):
        return 0

class Serial_tests():
    def wait(self):
        return 0

class Matrix_rank_test():
    def wait(self):
        return 0

class Compress_test():
    def wait(self):
        return 0

def main():
    name = "qe.xlsx"
    data = open("./" + name, "rb").read()
    fr = Frequency()
    fr.Init(data)
    print("n0 = ", fr.n0, "\nn1", fr.n1, "\nn_all = ", fr.n_all, "\nmap = ", fr.fr_map)

    return 0

main()
