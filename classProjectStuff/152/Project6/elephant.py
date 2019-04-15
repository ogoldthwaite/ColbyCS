#Owen Goldthwaite
#10/4/17
#CS 152 Project 5
#
# File Name: 
# File Purpose: 
#
# Unix Command: 

import random
import sys

IDXcalvingInt = 0
IDXpercentDarted = 1
IDXjuvAge = 2
IDXmaxAge = 3
IDXcalfSurv = 4
IDXadultSurv = 5
IDXseniorSurv = 6
IDXcapacity = 7
IDXyears = 8

IDXgender = 0
IDXage = 1
IDXmonthsPregnant = 2
IDXmonthsContra = 3

def initParameters():
    '''
      Initializes and returns the parameters list
    '''
    calvingInt = 3.1
    percentDarted = 0.0
    juvAge = 12
    maxAge = 60
    calfSurv = 0.85
    adultSurv = 0.996
    seniorSurv = 0.20
    capacity = 2000
    years = 200
    
    parameters = [calvingInt, percentDarted, juvAge, maxAge, calfSurv, adultSurv, 
                  seniorSurv, capacity, years]
                  
    return parameters

def interpretFlags(argv):
	'''
	  Interprets the user input of argv and edits the array parameters accordingly.
	'''
	parameters = initParameters()
	
	if("help" in argv):
		showHelp()
		exit()
	
	for i in range(len(argv)):
		if argv[i] == '-i':
			parameters[IDXcalvingInt] = float(argv[i+1])
		if argv[i] == '-p':
			parameters[IDXpercentDarted] = float(argv[i+1])
		if argv[i] == '-j':
			parameters[IDXjuvAge] = int(argv[i+1])
		if argv[i] == '-m':
			parameters[IDXmaxAge] = int(argv[i+1])
		if argv[i] == '-v':
			parameters[IDXcalfSurv] = float(argv[i+1])
		if argv[i] == '-a':
			parameters[IDXadultSurv] = float(argv[i+1])
		if argv[i] == '-s':
			parameters[IDXseniorSurv] = float(argv[i+1])
		if argv[i] == '-c':
			parameters[IDXcapacity] = int(argv[i+1])
		if argv[i] == '-y':
			parameters[IDXyears] = int(argv[i+1])
		
	return parameters

def showHelp():
	'''
	  Just prints the help text to reduce clutter in the flags method.
	'''
	print("HELP WINDOW: ")
	print("Default Usage: python3 elephant.py")
	print("Flags: ")
	print("-i <float> specifies the calving interval")
	print("-p <float> specifies the percent darted")
	print("-j <int> specifies the juvenile age")
	print("-m <int> specifies the max age")
	print("-v <float> specifies the calf survival rate")
	print("-a <float> specifies the adult survival rate")
	print("-s <float> specifies the senior survival rate")
	print("-c <int> specifies the max capacity")
	print("-y <int> specifies the amount of years to run")
	
	return	

def isFemale(elephant):
    '''
      Returns true if an elephant is female, false otherwise
    '''
    return (elephant[IDXgender] == 'f')

def isBreedingAge(parameters, elephant):
    '''
      Returns true if an elephant is within breeding age, false otherwise
    '''
    return ((elephant[IDXage] > parameters[IDXjuvAge]) and (elephant[IDXage] <= parameters[IDXmaxAge]))
    
def checkAge(elephant):
    '''
      Returns -2 if elephant is calf, -1 if elephant is juvenile, 0 if elephant is adult, 1 if elephant is senior
    '''
    age = elephant[IDXage]
    
    if(age <= 1):
        return -2
    elif age <= 12:
        return -1
    elif age <= 60:
        return 0
    else:
        return 1
        
def didSurvive(parameters, elephant):
    '''
      Checks if a given elephant will survive to the next year, returns a boolean true or false.
    '''
    if(checkAge(elephant) == -2):
        if(random.random() < parameters[IDXcalfSurv]):
            return True
    elif(checkAge(elephant) == -1):
        if(random.random() < parameters[IDXadultSurv]):
            return True
    elif(checkAge(elephant) == 0):
        if(random.random() < parameters[IDXadultSurv]):
            return True
    else:
        if(random.random() < parameters[IDXseniorSurv]):
            return True
    
    return False

def newElephant(parameters, age):
    '''
      Generates a new elephant of age age and returns it
    '''
    calvingInt = parameters[IDXcalvingInt]
    juvAge = parameters[IDXjuvAge]
    maxAge = parameters[IDXmaxAge] 
    
    
    elephant = 4 * [0]
    
    if(random.random() < 0.5):
        elephant[IDXgender] = 'f'
    else:
        elephant[IDXgender] = 'm'
    
    elephant[IDXage] = age
    
    if(isFemale(elephant)):
        if(isBreedingAge(parameters, elephant)):
            if(random.random() < (1.0/calvingInt)):
                elephant[IDXmonthsPregnant] = random.randint(1,22)
                
    return elephant

def initPopulation(parameters):
    '''
      Initializes a population of elephants!
    '''
    
    population = []
    
    for x in range(parameters[IDXcapacity]):
        population.append(newElephant(parameters, random.randint(1, parameters[IDXmaxAge])))
        
    return population

def incrementAge(population):
    '''
      Increments each elephant in list populations age by 1. Population is a list of elephants
    '''
    for i in range(len(population)):
        population[i][IDXage] += 1
        
    return population
    
def calcSurvival(parameters, population):
    '''
      Determines what elephants survive to the next year.
    '''
    newPop = []
    
    for elephant in population:
        if(didSurvive(parameters, elephant)):
            newPop.append(elephant)
    
    return newPop
    
def dartElephants(parameters, population):
    '''
      Checks adult females and randomly selects individuals to dart, returns pop.
    '''
    dartProb = parameters[IDXpercentDarted]
    
    for elephant in population:
        if(checkAge(elephant) == 0):
            if(random.random() < dartProb):
                elephant[IDXmonthsPregnant] = 0
                elephant[IDXmonthsContra] = 22
    
    return population

def cullElephants(parameters, population):
    '''
      Removes randomly chosen elephants from the list and returns the new population and
      the number of elephants killed
    '''
    carryCap = parameters[IDXcapacity]
    newPop = population
    
    if(len(population) > carryCap):
        random.shuffle(population)
        newPop = population[:carryCap]
    
    return (newPop, len(population[carryCap:]))

def controlPopulation(parameters, population):
    '''
      Determines whether population should be darted or culled and performs proper task
    '''
    if(parameters[IDXpercentDarted] == 0):
        (newPop, numCulled) = cullElephants(parameters, population)
    else:
        newPop = dartElephants(parameters, population)
        numCulled = 0
    
    return (newPop, numCulled)

def simulateMonth(parameters, population):
    '''
      Simulates one month of the simulation and returns new population.
      Checks for pregnancy/contraceptive and all that jazz.
    '''
    calvInt = parameters[IDXcalvingInt]
    
    for e in population:
        gender = e[IDXgender]
        age = e[IDXage]
        monthsPregnant = e[IDXmonthsPregnant]
        monthsContra = e[IDXmonthsContra]

        if((isFemale(e)) and (checkAge(e) == 0)):
            if(monthsContra > 0):               
                e[IDXmonthsContra] -= 1
            elif(monthsPregnant > 0):
                if(monthsPregnant >= 22):
                    population.append(newElephant(parameters, 1))
                    e[IDXmonthsPregnant] = 0
                # else
                else:
                    e[IDXmonthsPregnant] += 1
            # else
            else:
                if(random.random() < (1.0/(calvInt*12 - 22))):
                    e[IDXmonthsPregnant] = 1
                    
    return population
    
def simulateYear(parameters, population):
	'''
	  Simulates one year of simulation.
	'''
	population = calcSurvival(parameters, population)
	population = incrementAge(population)
	
	for i in range(12):
		population = simulateMonth(parameters, population)
		
	return population
	
def calcResults(parameters, population, numCulled):
	'''
	  Calculates how many elephants of each age group are in pop, then returns a list of those 
	  values along with total pop and number culled.
	'''
	calves = 0
	juvs = 0
	mAdults = 0
	fAdults = 0
	seniors = 0
	
	for e in population:
		age = checkAge(e)
		if(age == -2):
			calves += 1
		elif(age == -1):
			juvs += 1
		elif(age == 0 and (not(isFemale(e)))):
			mAdults += 1
		elif(age == 0 and (isFemale(e))):
			fAdults += 1
		else:
			seniors += 1
			
	results = [len(population), calves, juvs, mAdults, fAdults, seniors, numCulled]
	return results

def runSimulation(parameters):
    '''
      Runs the simulation for parameters[IDXyear] years.
    '''
    popsize = parameters[IDXcapacity]

    # init the population
    population = initPopulation(parameters)
    [population,numCulled] = controlPopulation( parameters, population )

    # run the simulation for N years, storing the results
    results = []
    for i in range(parameters[IDXyears]):
        population = simulateYear( parameters, population )
        [population,numCulled] = controlPopulation( parameters, population )
        results.append( calcResults( parameters, population, numCulled ) )
        if results[i][0] > (2 * popsize) or results[i][0] == 0 : # cancel early, out of control
            print('Terminating early')
            break
        
    return results

def getAverages(results):
    '''
      Solves for average values in the result list and returns them in a list averages
    '''
    answer = 7 * [0]

    for year in results:
        for i in range(len(year)):
            answer[i] += year[i]

    for i in range(len(answer)):
        answer[i] = answer[i] / len(results)

    return answer

def elephantSim(percDart, inputParameters = None):
    '''
      Does elephant stuff
    '''
    
    if(inputParameters == None):
        parameters = initParameters()
    else:
        parameters = inputParameters
        
    parameters[IDXpercentDarted] = percDart
        
    results = runSimulation(parameters)
    for i in range(4):
            results += runSimulation(parameters)    
            
    avgPop = 0
    for list in results:
        avgPop += list[0]
        
    avgPop = avgPop / len(results)    
        
    return int(parameters[IDXcapacity] - avgPop)

def test(): 
    '''
      Does stuff!
    '''
    parameters = initParameters()
                  
    #print(parameters)
    #print(parameters[IDXcapacity])
    
    pop = []
    for i in range(15):
        pop.append( newElephant( parameters, random.randint(1, parameters[IDXmaxAge]) ) )

    #for e in pop:
        #print(e)
        
    pop = initPopulation(parameters)
    
    for e in pop:
        print(e)
       
    print()    
    pop = incrementAge(pop)
    
    for e in pop:
        print(e)
    
def main(argv):
    '''
      Does main stuff!
    '''
    parameters = interpretFlags(argv)
    #Dart Prob of 43% seems to be pretty stable for 6500 - 8000

    results = runSimulation(parameters)
    print(results[-1])
    averages = getAverages(results)

    print("Average Total Population: ", averages[0])
    print("Average Calf Population: ", averages[1])
    print("Average Juvenile Population: ", averages[2])
    print("Average Male Adult Population: ", averages[3])
    print("Average Female Adult Population: ", averages[4])
    print("Average Senior Population: ", averages[5])
    print("Average Number Culled: ", averages[6])

if __name__ == "__main__":
    main(sys.argv)
    #test()
                  
