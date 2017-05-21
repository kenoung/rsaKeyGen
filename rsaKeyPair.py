#!/usr/bin/env python
"""
Generates RSA Key pairs.

>>> generator = RSAKeyPairGenerator()
>>> generator.generate_keys()
"""
from randomPrimeGenerator import RandomPrimeGenerator
from fractions import gcd

class RSAKeyPairGenerator():
    """
    Generates RSA Key Pairs from random numbers obtained from Random.org.

    References wikipedia: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
    """
    def __init__(self):
        self.primeGenerator = RandomPrimeGenerator()
        self.p = None
        self.q = None
        self.n = None
        self.lcm = None
        self.e = None
        self.d = None
        self.public = None
        self.private = None

    def generate_keys(self):
        self.p = self.primeGenerator.get_random_prime()
        self.q = self.primeGenerator.get_random_prime()
        self.n = self.p * self.q
        self.lcm = self.n // gcd(self.p, self.q)
        self.e = self.find_e(self.lcm)
        self.d = mulinv(self.e, self.lcm)

        self.public = (self.n, self.e)
        self.private = (self.n, self.d)
        return self.public, self.private

    def find_e(self, lcm):
        for i in range(3, lcm, 2):
            if gcd(i, lcm) == 1:
                return i


# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def mulinv(b, n):
    g, x, _ = xgcd(b, n)
    if g == 1:
        return x % n


    

