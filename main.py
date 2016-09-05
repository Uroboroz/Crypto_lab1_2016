# -*- coding:utf-8 -*-
import random

'''

1. Подстановка
2. Перестановка
3. Гамирование (шифр Виженера)

'''

class Substitution_cipher():
    key_map = {}
    abc = {}

    @staticmethod
    def random_list(list_):
        ret = []
        while len(list_) > 0:
            ret.append(random.choice(list_))
            list_.remove(ret[len(ret)-1])
        return ret

    def key_generator(self, data):
        key_, val_ = [], []
        for s in data:
            self.abc[s] = s
            key_.append(s)
            val_.append(s)

        self.key_map = dict(zip(self.random_list(key_), self.random_list(val_)))

    def encrypt(self, data):
        self.key_generator(data)
        encrypt_data = ""
        for s in data:
            encrypt_data += self.key_map[s]
        return encrypt_data

    def decrypt(self, data, key_map):
        self.key_map = key_map
        decrypt_data = ""
        key_reverse = {v: k for k, v in self.key_map.items()}
        for s in data:
            decrypt_data += key_reverse[s]
        return decrypt_data

class Transposition_cipher():
    key_map = {}
    i = 0

    @staticmethod
    def random_list(list_):
        ret = []
        while len(list_) > 0:
            ret.append(random.choice(list_))
            list_.remove(ret[len(ret)-1])
        return ret

    def key_generator(self, data):
        self.i = int(random.uniform(5, len(data)-1))
        self.key_map = dict(zip(self.random_list(list(range(self.i))), self.random_list(list(range(self.i)))))

    def encrypt(self, data):
        self.key_generator(data)
        encrypt_data = ""
        if len(data) % self.i != 0:
            data += " "*(self.i - len(data) % self.i)
        for s in range(0, len(data), self.i):
            temp = ""
            for i in range(self.i):
                temp += data[s+self.key_map[i]]
            encrypt_data += temp
        return encrypt_data

    def decrypt(self, data, key_map):
        self.key_map = key_map
        decrypt_data = ""
        key_reverse = {v: k for k, v in self.key_map.items()}
        for s in range(0, len(data), self.i):
            temp = ""
            for i in range(self.i):
                temp += data[s+key_reverse[i]]
            decrypt_data += temp
        return decrypt_data.strip()

class Vigenere_cipher():
    key_string = ""

    def xor_strings(self, xs, ys):
        if len(xs) % len(self.key_string) != 0:
            xs += " "*(len(self.key_string) - len(xs) % len(self.key_string))
        result = ""
        for i in range(len(ys)):
            result += chr(ord(xs[i]) ^ ord(ys[i]))
        return result

    def key_generator(self, data):
        self.key_string += "".join([chr(int(random.uniform(0, 256))) for i in range(int(random.uniform(2, len(data))))])
        print(self.key_string)
        return self.key_string

    def encrypt(self, data):
        return self.xor_strings(data, self.key_generator(data))

    def decrypt(self, data, key_string):
        self.key_string = key_string
        return self.xor_strings(data, self.key_string).strip()

def main():
    name = "./data.txt"
    data = open(name).read()

    ###########################################
    #                                         #
    #           SUBSTITUTION CIPHER           #
    #                                         #
    ###########################################

    sub_ciph = Substitution_cipher()
    print("Data    :", data)
    print("Encrypt :", sub_ciph.encrypt(data))
    open(name+".sub.enc", "w").write(sub_ciph.encrypt(data))

    print("Decrypt :", sub_ciph.decrypt(sub_ciph.encrypt(data), sub_ciph.key_map))
    open(name+".sub.dec", "w").write(sub_ciph.decrypt(sub_ciph.encrypt(data), sub_ciph.key_map))

    print("Key =", sub_ciph.key_map)
    open(name+".sub.key", "w").write(str(sub_ciph.key_map))

    if data == sub_ciph.decrypt(sub_ciph.encrypt(data), sub_ciph.key_map):
        print("Data == Decrypt")
    #print("ABC =", sub_ciph.abc)


    ###########################################
    #                                         #
    #          TRANSPOSITION CIPHER           #
    #                                         #
    ###########################################

    tr_ciph = Transposition_cipher()
    print("\nData    :", data)
    print("Encrypt :", tr_ciph.encrypt(data))
    open(name+".tr.enc", "w").write(tr_ciph.encrypt(data))

    print("Decrypt :", tr_ciph.decrypt(tr_ciph.encrypt(data), tr_ciph.key_map))
    open(name+".tr.dec", "w").write(tr_ciph.decrypt(tr_ciph.encrypt(data), tr_ciph.key_map))

    print("Key =", tr_ciph.key_map)
    open(name+".tr.key", "w").write(str(tr_ciph.key_map))
    #if data == sub_ciph.decrypt(sub_ciph.encrypt(data), sub_ciph.key_map):
    #    print("Data == Decrypt")

    ###########################################
    #                                         #
    #             VIGENERE CIPHER             #
    #                                         #
    ###########################################

    vz_ciph = Vigenere_cipher()
    print("\nData    :", data)
    print("Encrypt :", vz_ciph.encrypt(data))
    print("Decrypt :", vz_ciph.decrypt(vz_ciph.encrypt(data), vz_ciph.key_string))
    print("Key =", vz_ciph.key_string)
    #if data == sub_ciph.decrypt(sub_ciph.encrypt(data), sub_ciph.key_map):
    #    print("Data == Decrypt")


main()
