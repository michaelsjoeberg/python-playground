#!/usr/bin/python

# EXAMPLE: If-Else

import math
import os
import random
import re
import sys

# If  is odd, print Weird
# If  is even and in the inclusive range of 2 to 5, print Not Weird
# If  is even and in the inclusive range of 6 to 20, print Weird
# If  is even and greater than 20, print Not Weird

def is_it_weird(n):
    if (n >= 1 and n <= 100):
        if (n % 2 != 0):
            #print("Weird")
            return ("Weird")
        else:
            if (n >= 2 and n <= 5):
                #print("Not Weird")
                return ("Not Weird")
            elif (n >= 6 and n <= 20):
                #print("Weird")
                return ("Weird")
            elif (n > 20):
                #print("Not Weird")
                return ("Not Weird")

assert(is_it_weird(3) == "Weird")                   # OK
assert(is_it_weird(24) == "Not Weird")              # OK

if __name__ == '__main__':
    n = int(raw_input().strip())
    is_it_weird(n)