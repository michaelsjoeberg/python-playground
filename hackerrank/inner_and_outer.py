#!/usr/bin/python

import numpy as np

A = np.array([0, 1])
B = np.array([3, 4])

# inner
#print(np.inner(A, B))
# 4

# outer
#print(np.outer(A, B))
# [[0 0]
#  [3 4]]

# TEST
test_input = """0 1
2 3"""

A = test_input.split("\n")[0]
B = test_input.split("\n")[1]

A = list(map(int, A.split()))
B = list(map(int, B.split()))

print(np.inner(A, B))
print(np.outer(A, B))