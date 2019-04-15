# Bruce Maxwell
# Fall 2016
# CS 152 Project 7
#
# Test program for get/set functions
import simulation

# print out the simulation parameters nicely
def printSim(s):
    print("------------------")
    print( " percDart        :", s.getPercDart())
    print( " cullStrategy    :", s.getCullStrategy())
    print( " probCalfSurv    :", s.getProbCalfSurv())
    print( " probAdultSurv   :", s.getProbAdultSurv())
    print( " probSeniorSurv  :", s.getProbSeniorSurv())
    print( " calvingInterval :", s.getCalvingInterval())
    print( " carryingCapacity:", s.getCarryingCapacity())
    print( "------------------")

# main test function
def main():

    # create a new Simulation object
    sim = simulation.Simulation()

    # print the default values
    print("Defaults")
    printSim(sim)

    # use the set methods to change the parameter values
    sim.setPercDart(0.0)
    sim.setCullStrategy(1)
    sim.setProbCalfSurv(0.9)
    sim.setProbAdultSurv(0.995)
    sim.setProbSeniorSurv(0.3)
    sim.setCalvingInterval(3.3)
    sim.setCarryingCapacity(1000)

    # print the new values
    print("New values")
    printSim( sim )


# top level code
if __name__ == "__main__":
    main()
    
    
    
