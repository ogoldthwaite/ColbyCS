#Owen Goldthwaite
#9/13/2017
#CS 152 Project 2
#
# Command to run the program:
# grep /2014 blend.csv | cut -f 4,5 -d ',' | python3 temps.py
#

import sys


def main(stdin):
	'''
	  Finds average high/low temp of inputted data, then prints
	'''
	hisum = 0
	losum = 0
	count = 0
	buf = stdin.readline()
	
	while buf.strip() != '':
	
		#pull information from standard input into a string buffer
		count += 1 
		
		#splitting columns by comma delim
		words = buf.split(',')
		
		#casting data to float and summing
		hisum += float(words[0])
		losum += float(words[1])
		buf = stdin.readline()
	pass
	
	print("Average high temp: {0:7.3f}" .format(hisum/count))
	print("Average low temp: {0:8.3f}" .format(losum/count))
pass


if __name__ == "__main__":	  #if statement makes main only execute through terminal
	main(sys.stdin)