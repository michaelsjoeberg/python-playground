#!/usr/bin/python

# For all non-negative integers i < N, print i^2.

if __name__ == '__main__':
    n = int(raw_input())

    i = 0
    while i < n:
        print(i ** 2)
        i += 1