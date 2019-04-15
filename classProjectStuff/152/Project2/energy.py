#Owen Goldthwaite
#9/13/17
#CS 152 Project 2
#
# File Name: MLRC_19.csv
# File Purpose: Stores weather data!
# Unix Command: grep '5/[[:digit:]]\+/16' MLRC_19.csv | cut -d ',' -f 2,4,5,8 | python3 energy.py > energy.csv
#
import sys

def windGustVariation(wind, gust):
	'''
	  Finds the difference of highest gust - avg wind per day and returns the difference.
	  Used for extension 1.
	'''
	return gust - wind

def main(stdin):
	'''
	  Prints out average wind, average gust, and average par for May 2016 at 15 minute intervals
	'''
	wind = [0.0,0.0,0.0]
	gust = [0.0,0.0,0.0]
	par = [0.0,0.0,0.0]
  
  	count = 0
  	avgWindVariance = 0 #count and windVariance both used for extension
	datetime = ''

	buf =  stdin.readline()

	while buf.strip() != '':
		
		wind[2] = wind[1]
		wind[1] = wind[0]

		gust[2] = gust[1]
		gust[1] = gust[0]

		par[2] = par[1]
		par[1] = par[0]

		words = buf.split(',')

		datetime = words[0]
		wind[0] = float(words[1])
		gust[0] = float(words[2])
		par[0] = float(words[3])
		
		count += 1
		
		buf = stdin.readline()

		if (":00:" in datetime) or (":15:" in datetime) or (":30:" in datetime) or (":45:" in datetime):
			avgWind = (wind[0]+wind[1]+wind[2])/3
			avgGust = (gust[0]+gust[1]+gust[2])/3
			avgPar = (par[0]+par[1]+par[2])/3
			avgWindVariance = windGustVariation(avgWind, avgGust) #Finds average difference between wind and gust for extra comparison

			print(datetime,",",avgWind,",",avgGust,",",avgPar,",",avgWindVariance)
		pass
		

	

if __name__ == "__main__":
	main(sys.stdin)