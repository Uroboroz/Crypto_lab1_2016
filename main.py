# -*- coding:utf-8 -*-
import random

'''
1. Подстановка
2. Перестановка
3. Гамирование (шифр Виженера)
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

    @staticmethod
    def random_list(list_):
        ret = []
        while len(list_) > 0:
            ret.append(random.choice(list_))
            list_.remove(ret[len(ret) - 1])
        return ret

    def key_generator(self, data):
        self.i = int(random.uniform(5, len(data) - 1))
        self.key_map = dict(zip(self.random_list(list(range(self.i))), self.random_list(list(range(self.i)))))

    def encrypt(self, data):
        self.key_generator(data)
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
        for s in range(0, len(data), self.i):
            temp = b""
            for i in range(self.i):
                temp += bytes([data[s + key_reverse[i]]])
            decrypt_data += temp
        return decrypt_data[:len(decrypt_data) - self.i:]


class Vigenere_cipher():
    key_string = b""

    def xor_strings(self, xs, ys):
        if len(xs) % len(self.key_string) != 0:
            xs += b" " * (len(self.key_string) - len(xs) % len(self.key_string))
        result = b""
        for i in range(len(ys)):
            result += bytes([xs[i] ^ ys[i]])
        return result

    def key_generator(self, data):
        self.key_string = b"".join(
                [bytes([int(random.uniform(0, 256))]) for i in range(int(random.uniform(2, len(data))))])
        return self.key_string

    def encrypt(self, data):
        return self.xor_strings(data, self.key_generator(data))

    def decrypt(self, data, key_string):
        self.key_string = key_string
        return self.xor_strings(data, self.key_string).strip()


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
    file = open("./sub.key." + name, "w")
    file.write(str(sub_ciph.key_map))
    file.close()


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
    file = open("./tr.key." + name, "w")
    file.write(str(tr_ciph.key_map))
    file.close()


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
    file = open("./vz.key." + name, "wb")
    file.write(vz_ciph.key_string)
    file.close()


def main():
    name = input("Input path file: ")
    if name == "":
        name = "qe.xlsx"
    data = open("./" + name, "rb").read()
    Test_Substitution(name, data)
    Test_Transposition(name, data)
    Test_Vigener(name, data)


main()
