#Owen Goldthwaite
#10/18/17
#CS 152 Project 6
#
# File Name: 
# File Purpose: 
#
# Unix Command: 

import random
import sys
import elephant

def optimize(min, max, optfunc, parameters = None, tolerance = 0.001, maxIterations = 20, verbose=False):
    '''
      Optimizes stuff!
    '''
    done = False
    
    while done == False:
        testValue = (max + min)/2
        
        if(verbose):
            print(min)
            print(max)
            print(testValue, "Opt Test")
            
        result = optfunc(testValue, parameters)
        
        if(verbose):
            print(result, "Opt Result")
            
        if(result > 0):
            max = testValue
        elif(result < 0):
            min = testValue
        else:
            done = True
            
        if((max - min) < tolerance):
            done = True
            
        maxIterations -= 1
        
        if(maxIterations <= 0):
            done = True
        
    return testValue

def appendToCsv(data):
    '''
      Appends the info in data into .csv file
    '''
    fp = open( "answers.csv", "a")
    fp.write("Value, Percent Darted\n")

    for tup in data:
        toWrite = str(tup[0]) + ", " + str(tup[1]) + "\n"
        fp.write(toWrite)  
    
    fp.close()  


def appendToFile(data):
    '''
      Appends the given data to a file
    '''
    fp = open( "results.txt", "a") 
    fp.write(str(data) + ",")  
    fp.close()  

def evalParameterEffect(whichParameter, testMin, testMax, testStep, defaults=None, verbose=False):
    '''
      Automates process of evaluating effects of changing simulation parameters across different values. testMin is min value
      testMax is max. whichParameter is the parameter to change and testStep is the amount to increase by each time
    '''

    if(defaults == None):
        simParameters = elephant.initParameters()
    else:
        simParameters = defaults[:]

    results = []

    if verbose:
        print("Evaluating parameter {0:d} from {1:.3f} to {2:.3f} with step {3:.3f}".format(whichParameter, testMin, testMax, testStep))

    t = testMin

    while t < testMax:
        simParameters[whichParameter] = t
        percDart = optimize(0.0, 0.5, elephant.elephantSim, simParameters, tolerance = 0.01, maxIterations = 20, verbose=True)
        #appendToFile((t, percDart)) #appends to .txt file, .csv is better.
        results.append((t, percDart))
        
        if verbose:
            print("{0:8.3f} \t{1:8.3f}".format(t, percDart), "STUFF")
        t += testStep

    if verbose:
        print("Terminating")

    appendToCsv(results) #Appends to .csv, main append function       
    return results
    

if __name__ == "__main__":
    evalParameterEffect(elephant.IDXadultSurv, 0.98, 1.0, 0.001, verbose=True)
    print("hey")
    evalParameterEffect(elephant.IDXcalfSurv, 0.80, .90, 0.01)
    evalParameterEffect(elephant.IDXseniorSurv, 0.1, .5, 0.05)
    evalParameterEffect(elephant.IDXcalvingInt, 3.0, 3.4, 0.05)
    evalParameterEffect(elephant.IDXcapacity, 3500, 7000, 500)