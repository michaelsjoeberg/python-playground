# Given 2 sets of integers, M and N, print their symmetric difference 
# in ascending order. The term symmetric difference indicates those 
# values that exist in either M or N but do not exist in both.

import sys

stdin = list(sys.stdin.read().split("\n"))

set_N = set(list(stdin[1].split(" ")))
set_M = set(list(stdin[3].split(" ")))

sdiff = []
for i in (set_N ^ set_M):
    sdiff.append(int(i))

for i in sorted(sdiff):
    print(i)