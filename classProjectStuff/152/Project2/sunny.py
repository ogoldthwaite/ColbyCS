#Owen Goldthwaite
#9/13/17
#CS 152 Project 2
#
# File Name: MLRC_19.csv
# File Purpose: Stores weather data!
# Unix Command: grep '[567]/[[:digit:]]\+/16' MLRC_19.csv | grep '12:00' | cut -d ',' -f 8 | python3 sunny.py
# Extension Unix Cmd 1: grep '[567]/[[:digit:]]\+/16' MLRC_19.csv | grep '8:00' | cut -d ',' -f 8 | python3 sunny.py
# Extension Unix Cmd 2: grep '[567]/[[:digit:]]\+/16' MLRC_19.csv | grep '16:00' | cut -d ',' -f 8 | python3 sunny.py
# Extension Unix Cmd 3: grep '[567]/[[:digit:]]\+/16' MLRC_19.csv | grep '[789]:00' | cut -d ',' -f 8 | python3 sunny.py

import sys

def main(stdin):
	'''
	  Prints the number of sunny/cloudy days of May, June and July of 2016 and the average par of sunny/cloudy days
	'''
	sunNum = 0
	sunSum = 0
	cloudNum = 0
	cloudSum = 0

	buf = stdin.readline()

	while buf.strip() != '':
		par = float(buf)
		if par >= 800:
			sunNum += 1
			sunSum += par
		else:
			cloudNum += 1
			cloudSum += par
		buf =  stdin.readline()

	print("There were ",  sunNum,  " sunny days with an average PAR of ",  (sunSum/sunNum))
	print("There were ", cloudNum,	" cloudy days with an average PAR of ",	(cloudSum/cloudNum))

if __name__ == "__main__":
	main(sys.stdin)