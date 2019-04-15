# Owen Goldthwaite
# Fall 2017
# CS 152 Project 7
#
# First class design
#
# Simulation class

import sys
import random
import elephant as ele

class Simulation:

    def __init__(self, percDart = 0.425, cullStrategy = 1, probCalfSurv = 0.85,probAdultSurv = 0.996,
             probSeniorSurv = 0.2, calvingInterval = 3.1, carryingCapacity = 7000):
    
        self.percDart = percDart
        self.cullStrategy = cullStrategy
        self.probCalfSurv = probCalfSurv
        self.probAdultSurv = probAdultSurv
        self.probSeniorSurv = probSeniorSurv
        self.calvingInterval = calvingInterval
        self.carryingCapacity = carryingCapacity
        self.population = []
        self.results = []

    #Get those gets
    def getPercDart(self):
        return self.percDart

    def getCullStrategy(self):
        return self.cullStrategy

    def getProbCalfSurv(self):
        return self.probCalfSurv

    def getProbAdultSurv(self):
        return self.probAdultSurv

    def getProbSeniorSurv(self):
        return self.probSeniorSurv

    def getCalvingInterval(self):
        return self.calvingInterval

    def getCarryingCapacity(self):
        return self.carryingCapacity

    #Set those sets!
    def setPercDart(self, val):
        self.percDart = val

    def setCullStrategy(self, val):
        self.cullStrategy = val

    def setProbCalfSurv(self, val):
        self.probCalfSurv = val

    def setProbAdultSurv(self, val):
        self.probAdultSurv = val

    def setProbSeniorSurv(self, val):
        self.probSeniorSurv = val

    def setCalvingInterval(self, val):
        self.calvingInterval = val

    def setCarryingCapacity(self, val):
        self.carryingCapacity = val

    #Methods that do stuff
    def initPopulation(self):
        '''
          Initializes the population
        '''
        for i in range(self.carryingCapacity):
            self.population.append(ele.Elephant(self.calvingInterval))

    def showPopulation(self):
        '''
          Just prints every elephant in the population list
        '''
        print("---Printing Population---")
        for elephant in self.population:
            print(elephant)

    def incrementAge(self):
        '''
          Increments the age of every elephant in the population.
        '''
        for elephant in self.population:
            elephant.incrementAge()

    def dartPopulation(self):
        for elephant in self.population:
            if((elephant.isFemale()) and (elephant.isAdult) and (random.random() < self.percDart)):
                elephant.dart()

    def cullElephants_0(self):
        '''
          Culls those elephants!
        '''
        toReturn = len(self.population) - self.carryingCapacity

        if(len(self.population) > self.carryingCapacity):
            random.shuffle(self.population)
            self.population = self.population[:self.carryingCapacity]

        return toReturn

    def cullElephants_1(self):
        '''
          Culls those female adult elephants!
        '''
        toReturn = len(self.population) - self.carryingCapacity
        count = toReturn

        if(len(self.population) > self.carryingCapacity):
            random.shuffle(self.population)
            for i in range(count):
                if(self.population[i].isAdult() and self.population[i].isFemale()):
                    del self.population[i]

        return toReturn 

    def controlPopulation(self):
        '''
          Controls the population!
        '''
        if(self.percDart > 0):
            self.dartPopulation()
            return 0
        elif(self.cullStrategy == 1):
            return self.cullElephants_1()
        else:
            return self.cullElephants_0()

    def simulateMonth(self):
        '''
          Simulates a month!
        '''
        for elephant in self.population:
            if((elephant.isFemale()) and (elephant.isAdult())):
                if(elephant.progressMonth(self.calvingInterval) == True):
                    self.population.append(ele.Elephant(self.calvingInterval, 1))

    def calcSurvival(self):
        '''
          Calculates survival of elephants!
        '''
        tempPop = []
        for elephant in self.population:
            if((elephant.isCalf()) and (random.random() < self.probCalfSurv)):
                tempPop.append(elephant)
            elif((elephant.isJuvenile()) and (random.random() < self.probAdultSurv)):
                tempPop.append(elephant)
            elif((elephant.isAdult()) and (random.random() < self.probAdultSurv)):
                tempPop.append(elephant)
            elif((random.random() < self.probSeniorSurv)):
                tempPop.append(elephant)

            self.population = tempPop

    def simulateYear(self):
        self.calcSurvival()
        self.incrementAge()
        for i in range(12):
            self.simulateMonth()

    def decimate(self, percKill):
        '''
          Kills a lot of elephants using elephant killing magic. Percent killed is = to percKill
        '''
        if(percKill < 1):
            random.shuffle(self.population)
            toKill = int((len(self.population) * percKill))
            for i in range(toKill):
                del self.population[i]



    def calcResults(self, numCulled):
        '''
          Calculates how many elephants of each age group are in pop, then returns a list of those 
          values along with total pop and number culled.
        '''
        calves = 0
        juvs = 0
        mAdults = 0
        fAdults = 0
        seniors = 0
    
        for elephant in self.population:
            if(elephant.isCalf()):
                calves += 1
            elif(elephant.isJuvenile()):
                juvs += 1
            elif(elephant.isAdult() and (not(elephant.isFemale()))):
                mAdults += 1
            elif(elephant.isAdult() and (elephant.isFemale())):
                fAdults += 1
            else:
                seniors += 1
            
        print(len(self.population))
            
        results = [len(self.population), calves, juvs, mAdults, fAdults, seniors, numCulled]
        return results

    def runSimulation(self, numYears = 200, startFresh = True):
        '''
          Runs the simulation!!
        '''
        if(startFresh):
            self.initPopulation()
            numCulled = self.controlPopulation()
            self.results = []

        for i in range(numYears):
            self.simulateYear()
            numCulled = self.controlPopulation()
            self.results.append(self.calcResults(numCulled))
            # if ((self.results[0]) > (2 * self.carryingCapacity)) or ((self.results[0]) == 0): # cancel early, out of control
            #     print('Terminating early')
            #     break
        
        # if(startFresh):  #Comment out to run normally, uncomment to utilize decimate and post decimate rebuild
        #     self.decimate(.30)
        #     self.runSimulation(100, False)

        return self.results

    def writeDemographics(self, filename = "demographics.csv"):
        '''
        Appends the info in data into .csv file
        '''
        fp = open( filename, "w")
        fp.write("#year, #population, #calves, #juveniles, #mAdults, #fAdults, #seniors, #numCulled\n")
        count = 1

        for data in (self.results):
            toWrite = (str(count) + ", " + str(data[0]) + ", " + str(data[1]) + ", " + str(data[2]) 
                    + ", " + str(data[3]) + ", " + str(data[4]) + ", " + str(data[5]) + ", " + str(data[6]) +"\n")
            fp.write(toWrite)
            count += 1  
    
        fp.close()  

def test_simple():
    sim = Simulation()
    sim.setCarryingCapacity(20)
    sim.initPopulation()
    sim.showPopulation()
    sim.incrementAge()
    sim.dartPopulation()
    sim.showPopulation()

    sim.setCarryingCapacity(15)
    print( "numCulled:", sim.cullElephants_0() )
    sim.showPopulation()

if __name__ == "__main__":
    test_simple()