#!/usr/bin/python

# You are given a string S. 
# Your task is to find out if the string S contains: alphanumeric characters, alphabetical characters, digits, lowercase and uppercase characters.

# isalnum()
def check_isalnum(s):
    for char in s:
        if (char.isalnum()):
            print('True')
            return

    print('False')
    return

# isalpha()
def check_isalpha(s):
    for char in s:
        if (char.isalpha()):
            print('True')
            return

    print('False')
    return

# isdigit()
def check_isdigit(s):
    for char in s:
        if (char.isdigit()):
            print('True')
            return

    print('False')
    return

# islower()
def check_islower(s):
    for char in s:
        if (char.islower()):
            print('True')
            return

    print('False')
    return

# isupper()
def check_isupper(s):
    for char in s:
        if (char.isupper()):
            print('True')
            return

    print('False')
    return

if __name__ == '__main__':
    s = raw_input()

    check_isalnum(s)
    check_isalpha(s)
    check_isdigit(s)
    check_islower(s)
    check_isupper(s)

