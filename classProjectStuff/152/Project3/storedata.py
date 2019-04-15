#Owen Goldthwaite
#9/20/17
#CS 152 Project 3
#
# File Name: 
# File Purpose: 
#
# Unix Command: cat 2015-08-01-dosat.csv | python3 storedata.py

import sys
import stats

def main(stdin):

	myList = []

	buf =  stdin.readline()
	
	while buf != '':
		myList.append(float(buf))
		buf =  stdin.readline()

	mean = stats.mean(myList)
	print(mean)
	return

if __name__ == "__main__":
	main(sys.stdin)