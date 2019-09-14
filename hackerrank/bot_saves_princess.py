#!/usr/bin/python

# The first line contains an odd integer N (3 <= N < 100) denoting the size of the grid.
# This is followed by an NxN grid. Each cell is denoted by '-' (ascii value: 45).
# The bot position is denoted by 'm' and the princess position is denoted by 'p'.

test_input = """---
-m-
p--"""

grid = []
for line in test_input.split("\n"):
    grid.append(line)

for row in grid:
    print(row)

    if (row.find('p') != -1):
        # [row, col]
        p = [row.find('p'), grid.index(row)]
    if (row.find('m') != -1):
        # [row, col]
        m = [row.find('m'), grid.index(row)]

distance = [p[0] - m[0], p[1] - m[1]]
#print(distance)
# [-1, 1]

# col moves
while abs(distance[1]) > 0:
    if (distance[1] >= 1):
        print("DOWN")
        distance[1] -= 1
        
    if (distance[1] <= -1):
        print("UP")
        distance[1] += 1

# row moves
while abs(distance[0]) > 0:
    if (distance[0] >= 1):
        print("RIGHT")
        distance[0] -= 1
    
    if (distance[0] <= -1):
        print("LEFT")
        distance[0] += 1
