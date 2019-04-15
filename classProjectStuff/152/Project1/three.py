#Owen Goldthwaite
#9/8/17
#CS 152 Project 1, three

import sys

def sumThree(x, y, z):
    ans = (x+y+z)
    return ans
      #main code

print("version 5")
a=float(sys.stdin.readline())
b=float(sys.stdin.readline())
c=float(sys.stdin.readline())
print("sum", sumThree(a, b, c))
print("avg", (sumThree(a, b, c))/3.0)

