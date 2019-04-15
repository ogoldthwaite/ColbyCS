#Owen Goldthwaite
#10/18/17
#CS 152 Project 6
#
# File Name: 
# File Purpose: 
#
# Unix Command: 

import random

def searchSortedList( myList, value ):
    '''
      Searchs stuff
    '''
    done = False
    found = False
    count = 0
    maxIdx = len(myList) - 1
    minIdx = 0

    while done != True:
        count += 1

        testIndex = (maxIdx + minIdx) // 2     

        if(myList[testIndex] < value):
            minIdx = testIndex + 1
        elif(myList[testIndex] > value):
            maxIdx = testIndex - 1
        else:
            done = True
            found = True

        if(maxIdx < minIdx):
            done = True
            found = False

    return (found, count)
    
def test():
    
#    a = []
#    for i in range(10000):
#        a.append( random.randint(0,100000) )

#    a.append(42)

#   a.sort()

#    print(searchSortedList( a, 42 ))

    a = range(1000000000)
    print(searchSortedList( a, -1 ))

if __name__ == "__main__":
    test()