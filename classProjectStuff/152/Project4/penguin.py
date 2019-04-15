#Owen Goldthwaite
#9/27/17
#CS 152 Project 4
#
# File Name: penguin
# File Purpose: simulates a colony of penguins!
#
# Unix Command: python3 penguin.py help

import sys
import random

def initPopulation(initSize, femProb):
	'''
	  Creates a population of size initSize and adds males and females to the population
	  based upon the given probability of a female occuring, femProb. Then returns population.
	'''
	population = []
	
	for i in range(initSize):
		if (random.random() < femProb):
			population.append('f')
		else:
			population.append('m')
	
	return population

def simulateYear(pop, elNinoProb, stdRho, elNinoRho, femProb, maxCapacity):
	'''
	  Runs one year of simulation.
	'''
	elNinoYear = False
	
	if (random.random() < elNinoProb):
		elNinoYear = True
	
	newPop = []

	for peng in pop:
		if(len(newPop) > maxCapacity):
			break

		if (elNinoYear):
			if (random.random() < elNinoRho):
				newPop.append(peng)
		else:
			newPop.append(peng)
			if(random.random() < (stdRho - 1)):
				if(random.random() < femProb):
					newPop.append('f')
				else:
					newPop.append('m')
				
	return newPop
	
def runSimulation(N, initPopSize, femProb, elNinoProb, stdRho, elNinoRho, maxCapacity, minViable):
	'''
	  Runs simulation? N = numbers of years to run
	'''
	population = initPopulation(initPopSize, femProb)
	endDate = N
	
	for year in range(N):
		newPop = simulateYear(population, elNinoProb, stdRho, elNinoRho, femProb, maxCapacity)
		
		if( (not(len(newPop) > minViable)) or (not(('f' in newPop) or ('m' in newPop))) ):
			endDate = year
			break
			
		population = newPop
		
	return endDate

def computeCEPD(N, results):
	'''
	  Generates the CEPD list using N, the max number of years, and results, the results of running the simulation 
	  a number of times, then returns the CEPD, cepd. CEPD is made by testing if a pop went extinct early and if so
	  adding 1 to each CEPD term from the year the pop went extince to N. Each term in the list is then divided by
	  the total number of simulations. Therefore, the higher the index of a term in CEPD the more deaths occured by that
	  point and a higher number is stored.
	'''
	cepd = N * [0]

	for year in results:
		if year < N:
			for i in range(year, N):
				cepd[i] += 1

	for i in range(len(cepd)):
		cepd[i] = cepd[i] / (len(results) + 0.0)

	return cepd

def showHelp():
	'''
	  Just prints the help text to reduce clutter in the flags method.
	'''
	print("HELP WINDOW: ")
	print("Default Usage: python3 penguins.py (runs 10 times with 7 year el Nino average)")
	print("Flags: ")
	print("-s <int> specifies number of simulations to run")
	print("-i <int> specifies initial population size")
	print("-y <int> specifies how many years a simulation lasts")
	print("-f <float> specifies probability of new penguin being female")
	print("-e <float> specifies avg year gap betwen El Ninos")
	print("-r <float> specifies the stdRho")
	print("-n <float> specifies the ninoRho")
	print("-c <int> specifies the max capacity")
	print("-m <int> specifies min viable population")
	
	return
	
def initDefaultArguments():
	'''
	  Initializes some default arguments so there is never an argument that isnt initialized.
	'''
	arguments = []
	
	arguments.append(10)	  #number of simulations
	arguments.append(201)	  #number of years per simulation
	arguments.append(500)	  #initial population size
	arguments.append(.5)	  #probability of female penguin
	arguments.append(7.0)     #average yearly gap between el ninos
	arguments.append(1.188)	  #stdRho
	arguments.append(0.41)	  #ninoRho
	arguments.append(2000)	  #max capacity of pop
	arguments.append(10)	  #min viable pop size
	
	return arguments
	

def interpretFlags(argv):
	'''
	  Interprets the user input of argv and edits the array arguments accordingly.
	'''
	arguments = initDefaultArguments()
	
	if("help" in argv):
		showHelp()
		exit()
	
	for i in range(len(argv)):
		if argv[i] == '-s':
			arguments[0] = int(argv[i+1])
		if argv[i] == '-y':
			arguments[1] = int(argv[i+1])
		if argv[i] == '-i':
			arguments[2] = int(argv[i+1])
		if argv[i] == '-f':
			arguments[3] = float(argv[i+1])
		if (argv[i] == '-e') and (float(argv[i+1]) >= 1.0):
			arguments[4] = float(argv[i+1])
		if argv[i] == '-r':
			arguments[5] = float(argv[i+1])
		if argv[i] == '-n':
			arguments[6] = float(argv[i+1])
		if argv[i] == '-c':
			arguments[7] = int(argv[i+1])
		if argv[i] == '-m':
			arguments[8] = int(argv[i+1])
		
	return arguments

# test function for initPopulations
def test():
	popsize = 10
	probFemale = .5

	pop = initPopulation(popsize, probFemale)

	print(pop)
	print()
	
	newpop = simulateYear(pop, 1.0, 1.188, 0.4, 0.5, 2000)

	print("El Nino year")
	print(newpop)

	newpop = simulateYear(pop, 0.0, 1.188, 0.4, 0.5, 2000)

	print("Standard year")
	print(newpop)
	
	print()
	
	year = runSimulation(201, 500, 0.5, 1.0/7.0, 1.188, .41, 2000, 10)
	print("Run Sim")
	print(year)
	
def main(argv):
	'''
	  Main!
	'''
	arguments = interpretFlags(argv)
	
	result = []
	count = 1
	value = 0
	
	simNum = arguments[0]	
	years = arguments[1]
	initialSize = arguments[2]
	femProb = arguments[3]
	ninoProb = 1.0/arguments[4]
	stdRho = arguments[5]
	ninoRho = arguments[6]
	maxCapacity = arguments[7]
	minViable = arguments[8]
	
	for i in range(simNum):
		value = runSimulation(years, initialSize, femProb, ninoProb, stdRho, ninoRho, maxCapacity, minViable)
		result.append(value)
		if value < years:
			count += 1
	
	cepd = computeCEPD(years, result) #For my own use: cepd is basically the chance a pop dies off by that year. It has N (years) entries.
									  #See the docstring for some more info
	
	#print(result)
	print("Average Extincion Rate: ", count / (simNum + 0.0)) #Number printed is % of sims that went extinct before N years

	for i in range(0, len(cepd), 10):
		print(cepd[i])

	

if __name__ == "__main__":
	main(sys.argv)
	#test()