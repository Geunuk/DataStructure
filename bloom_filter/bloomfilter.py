# number of hash functions
k = 7
# number of bits
m = 200
# number of inserted elements
n = 10

# probability of false positive

# probability that a certain bit is not set to 1
# by a certain hash function during the insertion of an element
# 1 - 1/m

# probability that the bit is not set to 1 by any of the the hash function
# (1-1/m)**k

# after insert n elemnts, probability that a certain bit is still 0
# (1-1/m)***(k*n)

# probability that it is 1
# 1-(1-1/m)**(k*n)

# after compute k hash functions, the probability of all position is 1
# (1-(1-1/m)**(k*n))**k = (1-e**(-k*n/m))**k

import numpy as np
import math
import matplotlib.pyplot as plt
import mmh3
from bitarray import bitarray
"""
k = np.arange(200)
p = (1-np.e**(-k*n/m))**k
#p = (1-np.exp(-k*n/m))**k
print(np.min(p), k[np.argmin(p)])
plt.scatter(k, p)
#plt.show()
"""

class BloomFilter:
    def __init__(self, m,):
        self.m = m
        self.n = 0
        self.k = round(m/n * math.log(2))
        self.btary = bitarray(m)
        self.btary.setall(False)

    def __repr__(self):
        return self.btary.to01()

    def __str__(self):
        return "m = {0}  n = {1}  k = {2}\n{3}".format(
                self.m, self.n, self.k, self.btary.to01())
    def prob_false_pos(self, *args, optimal=False):
        m, n ,k = self.m, self.n , self.k
        print(*args)
        for i in args:
            print(i)
        for x, y in zip([m, n, k], args):
            x = y
        k = m/n*log(2) if optimal else self.k
        print("m : {0}  n : {1}  k : {2}".format(m, b ,k))
        return (1-math.e**(-k*n/m))**k

    def insert(self, value):
        self.n += 1
        h = BloomFilter._hash(value)
        for i in range(k):
            self.btary |= bitarray(BloomFilter._binarize(h[i], self.m))

    def check(self, value):
        value = bitarray(BloomFilter._binarize(value, self.m))
        print('value', value)
        print('btary', self.btary)
        return value == self.btary & value

    def initialize(self, value):
        self.btary.setall(False)

    @staticmethod
    def _binarize(value, m):
        return bin(value)[2:].zfill(m)

    @staticmethod
    def _hash(value):
        h = [0]*k
        h1, h2 = mmh3.hash64(bytes(value), signed=False)
        for i in range(k):
            h[i] = h1 + (i*h2)
        return h

if __name__ == '__main__':
    b = BloomFilter(200)
    b.insert(60)
