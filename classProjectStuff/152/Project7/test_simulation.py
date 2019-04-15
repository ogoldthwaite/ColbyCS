# Bruce Maxwell
# Fall 2016
# CS 152 Project 7
#
# test of Simulation class
import sys
import simulation

# main test function, expects one command line argument which is percent darted
def main(argv):
    if len(argv) < 2:
        print( "Usage: python %s <perc darted>" % (argv[0]) )
        exit(-1)

    # create a simulation using the default parameters
    sim = simulation.Simulation()

    # set the percent darted
    sim.setPercDart( float(argv[1]) )

    # run the simulation
    results = sim.runSimulation(200)

    # average some of the results
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

    # write the demographics data to a file
    sim.writeDemographics("demographics.csv")

if __name__ == "__main__":
    main(sys.argv)
