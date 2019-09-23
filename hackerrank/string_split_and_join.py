#!/usr/bin/python

# You are given a string. 
# Split the string on a " " (space) delimiter and join using a - hyphen.

def split_and_join(line):
    tmp_str = line.split(" ")

    return "-".join(tmp_str)

if __name__ == '__main__':
    line = raw_input()
    result = split_and_join(line)

    print result