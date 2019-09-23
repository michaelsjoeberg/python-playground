#!/usr/bin/python

# You are given a string and your task is to swap cases. 
# In other words, convert all lowercase letters to uppercase letters and vice versa.

def swap_case(s):
    tmp_str = ""
    for char in s:
        if (char.isupper()):
            tmp_str = tmp_str + char.lower()
        elif(char.islower()):
            tmp_str = tmp_str + char.upper()
        else:
            tmp_str = tmp_str + char

    return tmp_str

if __name__ == '__main__':
    s = raw_input()
    result = swap_case(s)
    print result