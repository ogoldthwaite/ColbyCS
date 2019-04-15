#Owen Goldthwaite
#9/27/17
#CS 152 Project 3
#
# File Name: 
# File Purpose: 
#
# Unix Command: 

import sys

def main(argv):

   if len(argv) < 3:
        print("Usage: python3 com.py <number> <number>")
        exit()

   num1 =  int(argv[1])
   num2 =  int(argv[2])

   print(num1 + num2)

   return

if __name__ == "__main__":
   main(sys.argv)