#!/usr/bin/python

# Without using any string methods, try to print the following: 123...N

def print_sequence(N):

    string = ""
    i = 0
    while i < N:
        string = string + str(i + 1)
        i += 1

    return string

assert(print_sequence(3) == "123")              # OK