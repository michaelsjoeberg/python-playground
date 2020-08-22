# There is an array of n integers. There are also 2 disjoint sets, A and B, each 
# containing m integers. You like all the integers in set A and dislike all the 
# integers in set B. Your initial happiness is 0. For each i integer in the array, 
# if i in A, you add 1 to your happiness. If i in B, you add -1 to your happiness. 
# Otherwise, your happiness does not change. Output your final happiness at the end.
# 
# Note: Since A and B are sets, they have no repeated elements. However, the array 
# might contain duplicate elements.

# example input
#
# 3 2       	: array size, set size
# 1 5 3     	: array
# 3 1       	: set A
# 5 7       	: set B

# each array int in set A -> +1
# each array int in set B -> -1

import sys
stdin = list(sys.stdin.read().split("\n"))

array_size, set_size = stdin[0].split(" ")
array = list(stdin[1].split(" "))
set_A = set(list(stdin[2].split(" ")))
set_B = set(list(stdin[3].split(" ")))

set_A -= set_B
set_B -= set_A

happiness = 0
for i in array:
    if i in set_A:
        happiness += 1
    if i in set_B:
        happiness -= 1

print(happiness)