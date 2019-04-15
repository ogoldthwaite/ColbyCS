#Owen Goldthwaite
#9/17/17
#CS 152 Project 2
#
# File Name: 3100.iSIC2016.csv
# File Purpose: Stores temperature information
#
# Unix Command: grep '5/[[:digit:]]\+/2016' 3100_iSIC2016.csv | cut -d ',' -f 1,8,17 | python3 mixing.py > mixing.csv


import sys

def main(stdin):
	'''
	  Finds and prints change in temperature between 1m and 7m on a given day   
	'''
	buf = stdin.readline()

	while buf.strip() != '':
		words = buf.split(',')
		temp1m = float(words[1])			#One extension asked to maybe use a list here? I'm assuming for the temps									#
		temp7m = float(words[2])    		#I did not use a list for temps because it seems pointless, but hopefully I won't lose credit! 
		change = (temp1m - temp7m)/temp7m	#I did use a list in part 5
		print(words[0], ",", change)
		buf = stdin.readline()

if __name__ == "__main__":
	main(sys.stdin)