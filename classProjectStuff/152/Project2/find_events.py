#Owen Goldthwaite
#9/17/17
#CS 152 Project 2
#
# File Name: blend.csv
# File Purpose: Stores info from mixing.csv and energy.csv
#
# Unix Command: cat blend.csv | python3 find_events.py

import sys

def main(stdin):
	'''
	  Looks for a temperature change greater than 5% and, if found, will 
	  print out the weather conditions for the last hour to see if any patterns between
	  weather and temperature appear.	
	'''
	
	mix = [0.0,0.0,0.0,0.0]
	wind = [0.0,0.0,0.0,0.0]
	gust = [0.0,0.0,0.0,0.0]
	par = [0.0,0.0,0.0,0.0]

	datetime = ''

	buf = stdin.readline()

	while buf.strip() != '':

		mix[3] = mix[2]
		mix[2] = mix[1]
		mix[1] = mix[0]

		wind[3] = wind[2]
		wind[2] = wind[1]
		wind[1] = wind[0]

		gust[3] = gust[2]
		gust[2] = gust[1]
		gust[1] = gust[0]

		par[3] = par[2]
		par[2] = par[1]
		par[1] = par[0]

		words = buf.split(',')
		datetime = words[0]
		mix[0] = float(words[1])
		wind[0] = float(words[3])
		gust[0] = float(words[4])
		par[0] = float(words[5])

		buf =  stdin.readline()

		if(mix[3] - mix[0] > 0.05):
			print(datetime) 
			print("Mix: ", mix[3] , mix[0])
			print("Wind: ", wind[0]+wind[1]+wind[2]+wind[3])
			print("Gust: ", gust[0]+gust[1]+gust[2]+gust[3])
			print("Par: ", par[0]+par[1]+par[2]+par[3])
			print()
		pass











if __name__ == "__main__":
	main(sys.stdin)