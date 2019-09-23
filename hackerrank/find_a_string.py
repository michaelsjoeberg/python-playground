#!/usr/bin/python

# The user enters a string and a substring.
# You have to print the number of times that the substring occurs in the given string.

import re

def count_substring(string, sub_string):
    result = [s.start() for s in re.finditer('(?=%s)' % (sub_string), string)]

    return len(result)

if __name__ == '__main__':
    string = raw_input().strip()
    sub_string = raw_input().strip()
    
    count = count_substring(string, sub_string)
    print count