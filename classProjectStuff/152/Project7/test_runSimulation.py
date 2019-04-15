# Bruce Maxwell
# CS 152 Fall 2016
# Project 7
#
# Test function for the Simulation class
#
import sys
import simulation 

def test(argv):
    if len(argv) < 2:
        print("Usage: python %s <perc darted>" % (argv[0]))
        exit(-1)

    sim = simulation.Simulation()

    sim.setPercDart( float(argv[1]) )
    sim.setCarryingCapacity(1000)
    
    results = sim.runSimulation()

    avgpop = 0.0
    avgcalf = 0.0
    avgcull = 0.0
    for item in results:
        avgpop += item[0]
        avgcalf += item[1]
        avgcull += item[-1]
    avgpop /= len(results)
    avgcalf /= len(results)
    avgcull /= len(results)

    print( "darted %.2f -> %d total %d calvs %d culls" % (sim.getPercDart(), int(avgpop), int(avgcalf), int(avgcull) ))

if __name__ == "__main__":
    test(sys.argv)
