# Stephanie Taylor
# Fall 2015 CS151 (Science)
# Project 5
# This module tests the calcResults function in elephant.py
# Call it like this:
#    python3 test_calcResults.py
#
#                                                                                                                              
#                                                                                                                                     
# NOTE: The following statistics were calculated in Python2, which seems to have had a slightly different                             
# random number generator. Your results will be close to the following, but will likely not match exactly.                            
#         
#
#
#
# Because I have seeded the random number generator, the output will be identical every time you run it. You should see:
# There are 300 total elephants and it reports 10 were culled
# There are 100 calves, 20 juveniles, 42 adult males, 39 adult females, and 99 seniors
# If you would like it to change from run to run, then comment out the call to random.seed.

import elephant
import random

def main():
    random.seed( 0 )
    calving_interval = 3.1
    pcnt_darted = 0.0
    juvenile_age = 12
    max_age = 60
    p_calf_survival = 0.85
    p_adult_survival = 0.996
    p_senior_survival = 0.2
    carrying_capacity = 10000
    params = [calving_interval, pcnt_darted, juvenile_age, max_age, p_calf_survival, p_adult_survival, p_senior_survival, carrying_capacity]

    min_ages = [1,2,max_age]
    max_ages = [1,max_age,100]

    pop = []
    for pop_idx in range(len(min_ages)):
        for i in range( 100 ):
            # Create a new elephant in the given age range. It may be male or female
            pop.append( [random.choice(['m','f']), random.randint(min_ages[pop_idx], max_ages[pop_idx] ),0,0 ])
            
    results = elephant.calcResults( params, pop, 10 )
    
    # The order of elements in results should be: numTotal, numCalves, numJuveniles, numFemaleAdults, numMaleAdults, numSeniors, numCulled
    print( "There are %d total elephants and it reports %d were culled" % (results[0], results[6]))
    print( "There are %d calves, %d juveniles, %d adult females, %d adult males, and %d seniors" % (results[1], results[2], results[3], results[4], results[5]))

if __name__ == '__main__':
    main()
