# Stephanie Taylor
# Fall 2015 CS151 (Science)
# Project 5
# This module tests the dartElephants function in elephant.py
# Call it like this:
#    python test_dartElephants.py
# Because I have seeded the random number generator, the output will be identical every time you run it. You should see:
# Test 1
# Out of 5089 adult female elephants, 2574 are darted, leading to a percentage of 0.506. It should be 0.500
# 
# Test 2
# Out of 5010 adult female elephants, 0 are darted, leading to a percentage of 0.000. It should be 0.000
# 
# Test 3
# Out of 4944 adult female elephants, 4944 are darted, leading to a percentage of 1.000. It should be 1.000
# If you would like it to change from run to run, then comment out the call to random.seed.

import elephant
import random

def testDarting( pcnt_darted ):
    calving_interval = 3.1
    juvenile_age = 12
    max_age = 60
    p_calf_survival = 0.85
    p_adult_survival = 0.996
    p_senior_survival = 0.2
    carrying_capacity = 10000

    params = [calving_interval, pcnt_darted, juvenile_age, max_age, p_calf_survival, p_adult_survival, p_senior_survival, carrying_capacity]

    # Create a new, undarted population
    pop = []
    for i in range( carrying_capacity ):
        # Create a new adult elephant. 
        pop.append( [random.choice(['m','f']), random.randint(juvenile_age+1, max_age ), 0, 0] )
    pop = elephant.dartElephants( params, pop )

    numF = 0
    numDarted = 0
    for e in pop:
        if e[0] == 'f':
            numF += 1
            if e[3] == 22:
                numDarted += 1
    print("Out of %d adult female elephants, %d are darted, leading to a percentage of %0.3f. It should be %0.3f" % (numF, numDarted, float(numDarted)/numF,pcnt_darted))

def main():
    random.seed( 0 )

    # Test the function with a darting percentage of 50%
    print("Test 1")
    testDarting( 0.5 )

    # Test the function with a darting percentage of 0%
    print("\nTest 2")
    testDarting( 0.0 )

    # Test the function with a darting percentage of 100%
    print("\nTest 3")
    testDarting( 1.0 )
    

if __name__ == '__main__':
    main()