# Stephanie Taylor
# Fall 2015 CS151 (Science)
# Project 5
# This module tests the cullElephants function in elephant.py
# Call it like this:
#    python3 test_cullElephants.py
# Because I have seeded the random number generator, the output will be identical every time you run it. You should see:
#
#
#
# NOTE: The following statistics were calculated in Python2, which seems to have had a slightly different                             
# random number generator. Your results will be close to the following, but will likely not match exactly. 
#
#
# Test 1
# We needed to cull 1000 elephants and 1000 elephants were culled
# Out of 1000 calves before culling, approximately 909 should remain after culling. 933 remain.
# 
# Test 2
# We needed to cull 0 elephants and 0 elephants were culled
# Out of 0 calves before culling, approximately 0 should remain after culling. 0 remain.
# 
# Test 3
# We needed to cull 10000 elephants and 10000 elephants were culled
# Out of 10000 calves before culling, approximately 5000 should remain after culling. 5019 remain.
# If you would like it to change from run to run, then comment out the call to random.seed.

import elephant
import random

def testCulling( population_overrun ):
    calving_interval = 3.1
    juvenile_age = 12
    max_age = 60
    p_calf_survival = 0.85
    p_adult_survival = 0.996
    p_senior_survival = 0.2
    carrying_capacity = 10000
    pcnt_darted = 0.0

    params = [calving_interval, pcnt_darted, juvenile_age, max_age, p_calf_survival, p_adult_survival, p_senior_survival, carrying_capacity]

    # Create a new, undarted population
    pop = []
    for i in range( carrying_capacity ):
        # Create a new adult elephant. 
        pop.append( [random.choice(['m','f']), random.randint(juvenile_age+1, max_age ), 0, 0] )
    for i in range( population_overrun ):
        # Create a new calf.
        pop.append( [random.choice(['m','f']), 1, 0, 0] )
    (pop, numCulled) = elephant.cullElephants( params, pop )

    print("We needed to cull %d elephants and %d elephants were culled" % (population_overrun, numCulled))
    
    # If the population has been properly culled, there will still be calves.
    numCalves = 0
    for e in pop:
        if e[1] == 1:
            numCalves += 1
    print( "Out of %d calves before culling, approximately %d should remain after culling. %d remain." % (population_overrun, int((1-float(population_overrun)/(carrying_capacity+population_overrun))*population_overrun), numCalves))

def main():
    random.seed( 0 )

    # Test the function with a population overrun of 1000
    print("Test 1")
    testCulling( 1000 )

    # Test the function with a population overrun of 0
    print("\nTest 2")
    testCulling( 0 )

    # Test the function with a population overrun of 10000
    print("\nTest 3")
    testCulling( 10000 )
    
if __name__ == '__main__':
    main()
