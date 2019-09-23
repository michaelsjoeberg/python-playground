#!/usr/bin/python

# You are given an immutable string, and you want to make changes to it.

# INPUT
# abracadabra
# 5 k

# OUTPUT
# abrackdabra

def mutate_string(string, position, character):
    tmp_lst = list(string)
    tmp_lst[position] = str(character)

    return "".join(tmp_lst)

if __name__ == '__main__':
    s = raw_input()
    i, c = raw_input().split()
    s_new = mutate_string(s, int(i), c)
    
    print s_new