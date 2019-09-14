#!/usr/bin/python

# Given an integer, n, and n space-separated integers as input, create a tuple, t, of those n integers.
# Then compute and print the result of hash(t).

if __name__ == '__main__':
    #n = int(input())
    #integer_list = map(int, input().split())

    test_input = "1 2 3"
    integer_list = list(map(int, test_input.split()))

    print(hash(tuple(integer_list)))