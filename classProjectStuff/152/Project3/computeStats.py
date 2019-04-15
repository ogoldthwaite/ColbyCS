#Owen Goldthwaite
#9/20/17
#CS 152 Project 3
#
# File Name: 3100_iSIC.csv
# File Purpose: Stores temperature and other data
# Program Purpose: Computes som statsss!
#
# Unix Command (June): grep '6/[1234567]\+/2017' 3100_iSIC.csv | cut -d ',' -f 3,9,15 | python3 computeStats.py
# Unix Command (July): grep '7/[1234567]\+/2017' 3100_iSIC.csv | cut -d ',' -f 3,9,15 | python3 computeStats.py
# Unix Command (August): 

import sys
import stats

def main(stdin): #All the commented out stuff was just used in the lab when making this program

	val1 = []
	#meterTemp2 = []
	#terrestrialPar = []
	
	buf =  stdin.readline()
	
	while buf != '':
		
		words = buf.split(',')
		
	    #terrestrialPar.append(float(words[0])) 
		val1.append(float(words[1]))
		#meterTemp2.append(float(words[2]))
		
		buf =  stdin.readline()

	print("Min Val: ",stats.min(val1))
	print("Max Val: ",stats.max(val1))
	print("Mean Val: ",stats.mean(val1))
	print("Standard Deviation: ", stats.stdev(val1))
	
	return

if __name__ == "__main__":
	main(sys.stdin)