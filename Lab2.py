# -*- coding:utf-8 -*-
import random, pickle

'''
1. Подстановка
2. Перестановка
3. Гамирование (шифр Виженера)
4. Шифрование циклическим побитовым сдвигом
'''


class Substitution_cipher():
    key_map = {}

    @staticmethod
    def random_list(list_):
        ret = []
        while len(list_) > 0:
            ret.append(random.choice(list_))
            list_.remove(ret[len(ret) - 1])
        return ret

    def key_generator1(self, data):
        key_, val_ = [], []
        for s in data:
            key_.append(s)
            val_.append(s)

        self.key_map = dict(zip(self.random_list(key_), self.random_list(val_)))

    def key_generator2(self):
        self.key_map = dict(zip(self.random_list(list(range(256))), self.random_list(list(range(256)))))

    def encrypt(self, data):
        self.key_generator2()
        with open('./sub.key', 'wb') as f:
            pickle.dump(self.key_map, f)
        encrypt_data = b""
        for s in data:
            encrypt_data += bytes([self.key_map[s]])
        return encrypt_data

    def decrypt(self, data, key_map):
        self.key_map = key_map
        decrypt_data = b""
        key_reverse = {v: k for k, v in self.key_map.items()}
        for s in data:
            decrypt_data += bytes([key_reverse[s]])
        return decrypt_data


class Transposition_cipher():
    key_map = {}
    i = 0
    len_ = 0

    @staticmethod
    def random_list(list_):
        ret = []
        while len(list_) > 0:
            ret.append(random.choice(list_))
            list_.remove(ret[len(ret) - 1])
        return ret

    def key_generator(self, data):
        if 100 > len(data) - 1:
            n = len(data) - 1
        else:
            n = 100
        self.i = int(random.uniform(5, n))
        self.key_map = dict(zip(self.random_list(list(range(self.i))), self.random_list(list(range(self.i)))))

    def encrypt(self, data):
        self.key_generator(data)
        with open('./tr.key', 'wb') as f:
            pickle.dump(self.key_map, f)
        self.len_ = len(data)
        encrypt_data = b""
        if len(data) % self.i != 0:
            data += b" " * (self.i - len(data) % self.i)
        for s in range(0, len(data), self.i):
            temp = b""
            for i in range(self.i):
                temp += bytes([data[s + self.key_map[i]]])
            encrypt_data += temp
        return encrypt_data

    def decrypt(self, data, key_map):
        self.key_map = key_map
        decrypt_data = b""
        key_reverse = {v: k for k, v in self.key_map.items()}
        for s in range(len(data)):
            decrypt_data += bytes(
                    [data[int(s / len(key_reverse)) * len(key_reverse) + key_reverse[s % len(key_reverse)]]])
        return decrypt_data[:self.len_:]


class Vigenere_cipher():
    key_string = b""
    len_ = 0

    def xor_strings(self, xs, mode):
        if len(xs) % len(self.key_string) != 0:
            xs += b" " * (len(self.key_string) - (len(xs) % len(self.key_string)))
        result = b""
        for i in range(len(xs)):
            result += bytes([xs[i] ^ self.key_string[i % len(self.key_string)]])
        if mode == "dec":
            return result[:self.len_:]
        else:
            return result

    def key_generator(self):
        self.key_string = b"".join(
                [bytes([int(random.uniform(0, 256))]) for i in range(int(random.uniform(2, self.len_)))])

    def encrypt(self, data):
        self.len_ = len(data)
        self.key_generator()
        with open('./vz.key', 'wb') as f:
            pickle.dump(self.key_string, f)
        return self.xor_strings(data, "enc")

    def decrypt(self, data, key_string):
        self.key_string = key_string
        return self.xor_strings(data, "dec")


class Shift_cipher():
    key_list = []
    len_ = 0

    @staticmethod
    def shifte(char, l):
        bin_char = "0" * (8 - len(bin(char)[2::])) + bin(char)[2::]
        '''print(bin_char, " => ", bin_char[l:8:1] + bin_char[0:l:1], " => ",
              str(bin_char[l:8:1] + bin_char[0:l:1])[8 - l:8:1] + str(bin_char[l:8:1] + bin_char[0:l:1])[0:8 - l:1])'''
        return int(bin_char[l:8:1] + bin_char[0:l:1], 2)

    @staticmethod
    def shiftd(char, l):
        bin_char = "0" * (8 - len(bin(char)[2::])) + bin(char)[2::]
        # print(bin_char, " => ", bin_char[l:8:1]+bin_char[0:l:1], " => ", bin_char[0:l:1]+bin_char[l:8:1])
        return int(bin_char[l:8:1] + bin_char[0:l:1], 2)

    def key_generator(self):
        self.key_list = [int(random.uniform(0, 8)) for i in range(int(random.uniform(2, 100)))]

    def encrypt(self, data):
        self.len_ = len(data)
        self.key_generator()
        with open('./shift.key', 'wb') as f:
            pickle.dump(self.key_list, f)
        encrypt_data = b""
        for i in range(self.len_):
            encrypt_data += bytes([self.shifte(data[i], self.key_list[i % len(self.key_list)])])
        return encrypt_data

    def decrypt(self, data, key_list):
        self.key_list = key_list
        decrypt_data = b""
        for i in range(self.len_):
            decrypt_data += bytes([self.shiftd(data[i], 8 - self.key_list[i % len(self.key_list)])])
        return decrypt_data[:self.len_:]


def Test_Substitution(name, data):
    ###########################################
    #                                         #
    #           SUBSTITUTION CIPHER           #
    #                                         #
    ###########################################

    sub_ciph = Substitution_cipher()
    print("Data    :", data)
    print("Encrypt :", sub_ciph.encrypt(data))
    file = open("./sub.enc." + name, "wb")
    file.write(sub_ciph.encrypt(data))
    file.close()

    print("Decrypt :", sub_ciph.decrypt(sub_ciph.encrypt(data), sub_ciph.key_map))
    file = open("./sub.dec." + name, "wb")
    file.write(sub_ciph.decrypt(sub_ciph.encrypt(data), sub_ciph.key_map))
    file.close()

    print("Key =", sub_ciph.key_map)


def Test_Transposition(name, data):
    ###########################################
    #                                         #
    #          TRANSPOSITION CIPHER           #
    #                                         #
    ###########################################

    tr_ciph = Transposition_cipher()
    print("\nData    :", data)
    print("Encrypt :", tr_ciph.encrypt(data))
    file = open("./tr.enc." + name, "wb")
    file.write(tr_ciph.encrypt(data))
    file.close()

    print("Decrypt :", tr_ciph.decrypt(tr_ciph.encrypt(data), tr_ciph.key_map))
    file = open("./tr.dec." + name, "wb")
    file.write(tr_ciph.decrypt(tr_ciph.encrypt(data), tr_ciph.key_map))
    file.close()

    print("Key =", tr_ciph.key_map)


def Test_Vigener(name, data):
    ###########################################
    #                                         #
    #             VIGENERE CIPHER             #
    #                                         #
    ###########################################

    vz_ciph = Vigenere_cipher()
    print("\nData    :", data)
    print("Encrypt :", vz_ciph.encrypt(data))
    file = open("./vz.enc." + name, "wb")
    file.write(vz_ciph.encrypt(data))
    file.close()

    print("Decrypt :", vz_ciph.decrypt(vz_ciph.encrypt(data), vz_ciph.key_string))
    file = open("./vz.dec." + name, "wb")
    file.write(vz_ciph.decrypt(vz_ciph.encrypt(data), vz_ciph.key_string))
    file.close()

    print("Key =", vz_ciph.key_string)


def Test_Shift(name, data):
    ###########################################
    #                                         #
    #              SHIFT CIPHER               #
    #                                         #
    ###########################################

    vz_ciph = Shift_cipher()
    print("\nData    :", data)
    print("Encrypt :", vz_ciph.encrypt(data))
    file = open("./shift.enc." + name, "wb")
    file.write(vz_ciph.encrypt(data))
    file.close()

    print("Decrypt :", vz_ciph.decrypt(vz_ciph.encrypt(data), vz_ciph.key_list))
    file = open("./shift.dec." + name, "wb")
    file.write(vz_ciph.decrypt(vz_ciph.encrypt(data), vz_ciph.key_list))
    file.close()

    print("Key =", vz_ciph.key_list)


def main():
    # name = input("Input path file: ")
    # if name == "":
    name = "qe.xlsx"
    data = open("./" + name, "rb").read()
    Test_Substitution(name, data)
    Test_Transposition(name, data)
    Test_Vigener(name, data)
    Test_Shift(name, data)

    print("Data:      ", data)

    sub = Substitution_cipher()
    tr = Transposition_cipher()
    vz = Vigenere_cipher()
    sh = Shift_cipher()
    sub1 = Substitution_cipher()
    tr1 = Transposition_cipher()
    vz1 = Vigenere_cipher()
    sh1 = Shift_cipher()
    sub2 = Substitution_cipher()
    tr2 = Transposition_cipher()
    vz2 = Vigenere_cipher()
    sh2 = Shift_cipher()

    en_data = sh2.encrypt(vz2.encrypt(tr2.encrypt(sub2.encrypt(
            sh1.encrypt(
                    vz1.encrypt(tr1.encrypt(sub1.encrypt(sh.encrypt(vz.encrypt(tr.encrypt(sub.encrypt(data))))))))))))
    print("Encrypto : ", en_data)
    print("Decrypto : ", sub.decrypt(tr.decrypt(vz.decrypt(sh.decrypt(
            sub1.decrypt(tr1.decrypt(
                    vz1.decrypt(sh1.decrypt(
                            sub2.decrypt(tr2.decrypt(vz2.decrypt(sh2.decrypt(en_data, sh2.key_list), vz2.key_string),
                                         tr2.key_map), sub2.key_map), sh1.key_list), vz1.key_string), tr1.key_map),
            sub1.key_map), sh.key_list), vz.key_string), tr.key_map), sub.key_map))


main()
