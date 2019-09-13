#!/usr/bin/python

# The first line contains the sum of the two numbers.
# The second line contains the difference of the two numbers (first - second).
# The third line contains the product of the two numbers.

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

assert(add(3, 2) == 5)              # OK
assert(subtract(3, 2) == 1)         # OK
assert(multiply(3, 2) == 6)         # OK

if __name__ == '__main__':
    a = int(raw_input())
    b = int(raw_input())

    print(a + b)
    print(a - b)
    print(a * b)
