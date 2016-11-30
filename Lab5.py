import math


class Users:
    e = 0
    d = 0

    p = 0
    q = 0

    c = 0
    m = 0

    def __init__(self):
        print(self.bin_pow(3, 30), 3 ** 30)
        # self.p = self.eratosfen(1000000)[-1]
        # self.q = self.eratosfen(1000000)[-2]
        self.p, self.q = self.number(10), self.number(11)
        self.n = self.p * self.q
        phi = (self.p - 1) * (self.q - 1)  # = self.phi(self.n)
        print(phi, self.n)

        self.e = 0
        for i in range(int(phi ** 0.5), phi + 1):
            e = self.euclid(phi, i)
            if e == 1:
                self.e = i
                break

        print("Находим Ko =", self.e)

        for i in range(2, phi + 1):
            if ((i * phi + 1) / self.e) != 0 and float(int(((i * phi + 1) / self.e))) == ((i * phi + 1) / self.e):
                self.d = int((i * phi + 1) / self.e)
                break

        print("Находим Kc =", self.d)

        self.m = 10000

        print("Расшифрование: M =", self.m)
        self.c = self.mod_pow(self.m, self.e, self.n)
        print("Шифрование: C =", self.c)
        self.m = self.mod_pow(self.c, self.d, self.n)
        print("Расшифрование: M =", self.m)

    @staticmethod
    def mod_pow(x, n, module):
        result = 1
        while n != 0:
            if n % 2 != 0:
                result *= x
                result %= module
                n -= 1
            else:
                x *= x
                x %= module
                n /= 2
        return result

    @staticmethod
    def mod_pov(a, n, module):
        res = 1
        a1 = a
        while n:
            if n & 1:
                res *= a1
                res %= module
            a1 *= a
            a1 %= module
            n >>= 1
            # print(n)
        return res % module

    @staticmethod
    def phi(n):
        res = n
        i = 2
        while i ** 2 <= n:
            i += 1
            if n % i == 0:
                while n % i == 0:
                    n /= i
                res -= res / i
        if n > 1:
            res -= res / n
        return res

    @staticmethod
    def eratosfen(n):
        a = [True for i in range(n)]
        for i in range(2, int(math.sqrt(n))):
            for j in range(i * 2, n, i):
                a[j] = False
        return [i for i in range(2, n) if a[i]]

    @staticmethod
    def bin_pow(a, n):
        res = 1
        while n:
            if n & 1:
                res *= a
            a *= a
            n >>= 1
        return res

    @staticmethod
    def number(n):
        return 5 * (n * n - n) + 1

    @staticmethod
    def euclid(a, b):
        while b:
            a, b = b, a % b
        return a


Users()
