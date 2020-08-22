# Rupal has a huge collection of country stamps. She decided to 
# count the total number of distinct country stamps in her 
# collection. She asked for your help. You pick the stamps one 
# by one from a stack of N country stamps.
#
# Find the total number of distinct country stamps.

import sys

stdin = list(sys.stdin.read().split("\n"))[1:]

set_countries = set(stdin)

print(len(set_countries))