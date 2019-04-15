#Owen Goldthwaite
#9/8/17
#CS 152 Project 1, addlots
#Added max/min temp finding extension

import sys

max = -sys.maxsize - 1
min = sys.maxsize
sum = 0.0
count = 0
nextval = (sys.stdin.readline())

def findMax(temp, cMax):  #Finds max temp
	if temp > cMax:
		cMax = temp
		pass
	return cMax

def findMin(temp, cMin):  #Finds min temp
	if temp < cMin:
		cMin = temp
		pass
	return cMin

while nextval.strip() != '':
	sum += float(nextval)
	max = findMax(float(nextval), max)
	min = findMin(float(nextval), min)
	count += 1
	nextval = (sys.stdin.readline())
	pass

print("Total Count: ", count)
print("Average: ", sum/count)
print("Max Temp: ", max)
print("Min Temp: ", min)