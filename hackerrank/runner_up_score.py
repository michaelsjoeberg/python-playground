#!/usr/bin/python

# The first line contains n.
# The second line contains an array A of n integers each separated by a space.

n = 5
A = ("2 3 6 6 5").split(" ")

def remove_max_value(lst, max_value):
   return [value for value in lst if value != max_value]

A = remove_max_value(A, max(A))

print(max(A))

if __name__ == '__main__':
    n = int(raw_input())
    arr = map(int, raw_input().split())

    arr = remove_max_value(arr, max(arr))

    print(max(arr))