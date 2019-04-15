#Owen Goldthwaite
#9/20/17
#CS 152 Project 3
#
# File Name: 
# File Purpose: 
#
# Unix Command: 

import sys
import math

def sum(myArray):
	'''
	  Sums up all values in array myArray and returns it
	'''
	sum = 0.0
	
	for val in myArray:
		sum += val
	
	return sum
	
def mean(myArray):
	'''
	  Returns the mean value of myArray
	'''
	mean = 0.0
	mean = (sum(myArray) / len(myArray))
	return mean
	
def max(myArray):
	'''
	  Returns the max value inside of myArray
	'''
	maxVal = (-sys.maxsize - 1)
	
	for val in myArray:
		if (val > maxVal):
			maxVal = (val)
	
	return maxVal
	 #Possibly Change max/min to not return floats
	
def min(myArray):
	'''
	  Returns the min value inside of myArray
	'''
	minVal = (sys.maxsize)
	
	for val in myArray:
		if (val < minVal):
			minVal = (val)
	
	return minVal
	
def variance(myArray):
	'''
	  Returns the variance of myArray
	'''
	listVariance = 0.0
	xBar = mean(myArray)
	tempVar = 0.0
	
	for val in myArray:
		tempVar += ((val - xBar)**2)
	
	
	listVariance = (tempVar / (len(myArray)-1))
	return listVariance
	
	
def stdev(myArray):
	'''
	  Returns the standard deviation of myArray
	'''
	
	return math.sqrt(variance(myArray))
	
	
def celsius2fahrenheit(tempC):
	'''
	  Converts celsius temp (tempC) to fahrenheit and returns it
	'''
	return (((9/5)*tempC) + 32)
	
def test():
	'''
	  Runs stuff !
	'''
	array1 = [1,2,3,4]
	
	print(sum(array1))
	print(mean(array1))
	print(max(array1))
	print(min(array1))
	print(variance(array1))
	print(stdev(array1))
	print(celsius2fahrenheit(-40))
	
	
if __name__ == "__main__":
	test()