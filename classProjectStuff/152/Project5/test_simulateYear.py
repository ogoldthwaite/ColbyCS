# Stephanie Taylor
# Fall 2015 CS151 (Science)
# Project 5
# This module tests the simulateMonth function in elephant.py
# Call it like this:
#    python3 test_simulateYear.py
#
#                                                                                                                              
#                                                                                                                                     
# NOTE: The following statistics were calculated in Python2, which seems to have had a slightly different                             
# random number generator. Your results will be close to the following, but will likely not match exactly.                            
#         
#
#
# Because I have seeded the random number generator, the output will be identical every time you run it. You should see:
# After 1 year of simulation, there are 107 elephants.
# After 2nd year of simulation, there are 118 elephants.
# Before I fixed my bug in simulateMonth, here was my output:
# After 1 year of simulation, there are 107 elephants.
# After 2nd year of simulation, there are 111 elephants.
# If you would like it to change from run to run, then comment out the call to random.seed.

import elephant
import random
    
def main():
    random.seed( 0 )
    calving_interval = 3.1
    pcnt_darted = 0.5
    juvenile_age = 12
    max_age = 60
    p_calf_survival = 0.85
    p_adult_survival = 0.996
    p_senior_survival = 0.2
    carrying_capacity = 100
    params = [calving_interval, pcnt_darted, juvenile_age, max_age, p_calf_survival, p_adult_survival, p_senior_survival, carrying_capacity]

    pop = []
    for i in range( carrying_capacity ):
        pop.append( elephant.newElephant( params, random.randint(juvenile_age+1, max_age ) ) )
        
    pop = elephant.simulateYear( params, pop )
    print("After 1 year of simulation, there are %d elephants." % (len(pop)))

    pop = elephant.simulateYear( params, pop )
    print("After 2nd year of simulation, there are %d elephants." % (len(pop)))

    
if __name__ == '__main__':
    main()
