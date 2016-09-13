# -*- coding:utf-8 -*-
import math, numpy, zipfile, re

'''
Криптографические тесты (NIST)
'''


class Frequency:
    n0 = 0
    n1 = 0
    n_all = 0
    fr_map = {}

    def init(self, data):
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


class Entropy:
    freq = Frequency
    A_bit = 0.0
    A_byte = 0.0

    def init(self, freq, data):
        if freq is not None:
            self.freq = freq
        elif data is not None:
            self.freq = Frequency()
            self.freq.init(data)
        else:
            print("Error! Input args!")
            return

        self.A_bit = -1 * (self.freq.n0 / self.freq.n_all) * math.log((self.freq.n0 / self.freq.n_all), 2) - 1 * (
            self.freq.n1 / self.freq.n_all) * math.log((self.freq.n1 / self.freq.n_all), 2)

        for s in self.freq.fr_map.values():
            if s != 0:
                self.A_byte += -1 * (s / (self.freq.n_all / 8)) * math.log((s / (self.freq.n_all / 8)), 2)


class Serial:
    map_serial = {}
    maximum = 0

    @staticmethod
    def bit_data(data):
        bits = ''
        for s in data:
            bits += "0" * (8 - len(bin(s)[2::])) + bin(s)[2::]
        return bits

    def init(self, data):
        bits = self.bit_data(data)
        counter = 0
        b = True
        for s in bits:
            if s is '1' and b:
                counter += 1
            elif s is '1' and not b:
                b = True
                if counter not in self.map_serial:
                    self.map_serial[counter] = 1
                else:
                    self.map_serial[counter] += 1
                counter = 1
            elif s is '0' and not b:
                counter += 1
            elif s is '0' and b:
                b = False
                if counter not in self.map_serial:
                    self.map_serial[counter] = 1
                else:
                    self.map_serial[counter] += 1
                counter = 1

        self.maximum = max(self.map_serial.keys(), key=int)


class Matrix_rank:
    m0 = 0
    m1 = 0

    @staticmethod
    def bit_data(data):
        bits = ''
        for s in data:
            bits += "0" * (8 - len(bin(s)[2::])) + bin(s)[2::]
        return bits

    def init(self, data):
        bits = self.bit_data(data)
        for i in range(0, int(len(bits)/1024)*1024, 1024):
            temp_array = [list(bits[x:x+32:1]) for x in range(i, i+1024, 32)]
            temp_array = [[int(x) for x in temp_array[i]] for i in range(len(temp_array))]
            if numpy.linalg.det(temp_array) == 0:
                self.m0 += 1
            else:
                self.m1 += 1


class Compress:
    size_uncompress = 0
    size_compress = 0
    per = 0.0

    def init(self, name):
        zipf = zipfile.ZipFile('./test.zip', 'w', zipfile.ZIP_DEFLATED)
        zipf.write("./"+name)
        info = zipf.infolist()[0]
        self.size_uncompress = int(re.search(" file_size=(\d*) ", str(info)).group(1))
        self.size_compress = int(re.search(" compress_size=(\d*)", str(info)).group(1))
        self.per = float(self.size_compress / self.size_uncompress)
        return 0


def main():
    name = "qe.xlsx"
    data = open("./" + name, "rb").read()
    fr = Frequency()
    fr.init(data)
    print("n0 = ", fr.n0, "\nn1 = ", fr.n1, "\nn_all = ", fr.n_all, "\nmap = ", fr.fr_map)

    ent = Entropy()
    # ent.init(None, data)
    ent.init(fr, None)
    print("\nH(bit) = ", ent.A_bit, "\nH(byte) = ", ent.A_byte)

    ser = Serial()
    ser.init(data)
    print("Map = ", ser.map_serial, "\nMax = ", ser.maximum)

    matr = Matrix_rank()
    matr.init(data)
    print("\nMatrix (det = 0) = ", matr.m0, "\nMatrix (det = 1) = ", matr.m1)

    cmp = Compress()
    cmp.init(name)
    print("\nPer compress = ", cmp.per*100, "%")

    return 0




main()
