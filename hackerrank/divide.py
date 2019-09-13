#!/usr/bin/python

# The first line should contain integer division,  // . The second line should contain float division,  / .

from __future__ import division

def integer_devision(a, b):
    return a // b

def float_division(a, b):
    return a / b

assert(integer_devision(4, 3) == 1)
assert(round(float_division(4, 3), 4) == 1.3333)

if __name__ == '__main__':
    a = int(raw_input())
    b = int(raw_input())

    print(a // b)
    print(a / b)