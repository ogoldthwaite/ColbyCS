#Owen Goldthwaite
#9/20/17
#CS 152 Project 3
#
# File Name: 3100_iSIC.csv
# File Purpose: Stores weather data!
# Program Purpose: Compute the thermocline!
#
# Unix Command: curl http://schupflab.colby.edu/buoy/3100_iSIC.csv | grep '06/02/2017' | grep -e ' 1:00' -e ' 2:00' | python3 thermocline.py
# Unix Command 2 (For hourly): 

import sys

def density(temps):
    '''
      Calculates the densities of each temp and adds them to rhos; then returns rhos
    '''
    rhos = []

    for t in temps:
        rhos.append(1000 * (1 - (t + 288.9414) * (t - 3.9863)**2 / (508929.2*(t + 68.12963))))

    return rhos
    

def f(x):
    '''
      Just a method to help with the derivative method
    '''
    return x**2

def derivative(x):
    '''
      takes the derivative of a value x and returns it
    '''
    h = 1.0/10000000000000.0
    yChange = f(x + h) - f(x)
    xChange = h
    return (yChange / xChange)
    
def thermocline_depth(temps, depths):
    '''
      Returns the thermocline depth using parameters temps and depths
    '''

    rhos =  density(temps)
    drho_dz = []

    for val in rhos:
        val = derivative(val)

    for i in (range(len(rhos) - 1)):
    	drho_dz.append((rhos[i+1] - rhos[i]) / (depths[i+1] - depths[i]))
        # print(temps[i], rhos[i], drho_dz[i])

    max_drho_dz = -sys.maxsize + 1
    maxindex = -1

    for i in range(len(drho_dz)):
        if drho_dz[i] > max_drho_dz:
            max_drho_dz =  drho_dz[i]
            maxindex = i

    thermoDepth = (depths[maxindex] + depths[maxindex + 1])/2

    return thermoDepth

def changeAverage(): # Extension 3
	'''
      User inputs string newTime to define what time frame the program should calculate the average depth over.
      Only currently works correctly when using hourly unix command (2).

      Does not work correctly, could not figure out how to handle input from file and user input at same time
      Just change return value instead.
	'''
#	newTime = 1
#	while (newTime >= 1) and (newTime <=24):
#		newTime = float(input('Please Enter a Valid Time Frame (1-24): '))
	
	return (1) #Change this value to change the time frame over which the average is calculated, keep at 1 for normal use
    

def main(stdin):
    '''
      Manages all the data and sends it to be calcualted using the thermocline method
      then prints the result.
    '''

    fields = [8, 11, 14, 17, 20, 23, 26]

    depths = [ 1, 3, 5, 7, 9, 11, 13 ]

    maxDepth = -sys.maxsize + 1
    minDepth = sys.maxsize
    
    timeFrame = changeAverage() # values used for extension 3
    totalDepth = 0 
    count = 0
    
    dateTime = ""
    maxTime = ""
    minTime = ""

    buf = stdin.readline()

    while buf.strip() != '':
        words = buf.split(',')

        dateTime = words[0]
        temps = []

        for i in range(len(depths)):
            temps.append(float(words[fields[i]]))

        depth = thermocline_depth(temps, depths)

        if depth > maxDepth:
            maxDepth = depth
            maxTime = dateTime

        if depth < minDepth:
            minDepth = depth
            minTime = dateTime

        if((timeFrame != 1) and (count < timeFrame-1)):
            totalDepth += depth
            count += 1
        elif(timeFrame == 1):
        	print(dateTime, ', ', depth)
        	count = 0
        else:
        	print(dateTime, ', ', (totalDepth / timeFrame))
        	totalDepth = 0
        	count = 0

        buf = stdin.readline()

    # print out the minimum and maximum thermocline depth and the corresponding date/time
    #print("Max Depth: ", maxTime, ', ', maxDepth)
    #print("Min Depth: ", minTime, ', ', minDepth)


if __name__ == "__main__":
    main(sys.stdin)