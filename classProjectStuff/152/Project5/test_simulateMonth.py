# Stephanie Taylor
# Fall 2015 CS151 (Science)
# Project 5
# This module tests the simulateMonth function in elephant.py
# Call it like this:
#    python3 test_simulateMonth.py
#
#
#                                                                                                                              
#                                                                                                                                     
# NOTE: The following statistics were calculated in Python2, which seems to have had a slightly different                             
# random number generator. Your results will be close to the following, but will likely not match exactly.                            
#         
#
#
# Because I have seeded the random number generator, the output will be identical every # time you run it. 
# You should see:
# In month 1, out of 7500 adult female elephants, 212 gave birth, leading to a birth rate of 0.0283. It should be 0.0147
# In month 1, out of 2500 adult female elephants who could become pregnant, 151 became pregnant this month, leading to a conception rate of 0.060. It should be 0.066
# In month 2, out of 1332 adult female elephants who could become pregnant, 76 became pregnant this month, leading to a conception rate of 0.057. It should be 0.066
# In an earlier version of my elephant.py, I was using the wrong code to determine births (I had "> 22" instead of ">= 22", as the instructions indicate). The output from that run was this:
# In month 1, out of 7500 adult female elephants, 112 gave birth, leading to a birth rate of 0.0149. It should be 0.0147
# In month 1, out of 2500 adult female elephants who could become pregnant, 151 became pregnant this month, leading to a conception rate of 0.060. It should be 0.066
# In month 2, out of 1272 adult female elephants who could become pregnant, 82 became pregnant this month, leading to a conception rate of 0.064. It should be 0.066
# If you would like it to change from run to run, then comment out the call to random.seed.

import elephant
import random

def countFemalesEligibleForPregnancy( params, pop ):
    numF = 0
    for e in pop:
        gender = e[0]
        age = e[1]
        monthsPregnant = e[2]
        monthsContraceptive = e[3]
        if gender == 'f' and age > params[2] and age <= params[3] and monthsPregnant == 0 and monthsContraceptive == 0:
            numF += 1
    return numF

def countFemalesNewlyPregnant( params, pop ):
    numF = 0
    for e in pop:
        gender = e[0]
        age = e[1]
        monthsPregnant = e[2]
        monthsContraceptive = e[3]
        if gender == 'f' and age > params[2] and age <= params[3] and monthsPregnant == 1:
            numF += 1
    return numF

def countAdultFemales( params, pop ):
    numF = 0
    for e in pop:
        gender = e[0]
        age = e[1]
        monthsPregnant = e[2]
        monthsContraceptive = e[3]
        if gender == 'f' and age > params[2] and age <= params[3]:
            numF += 1
    return numF
    
def main():
    random.seed( 0 )
    calving_interval = 3.1
    pcnt_darted = 0.5
    juvenile_age = 12
    max_age = 60
    p_calf_survival = 0.85
    p_adult_survival = 0.996
    p_senior_survival = 0.2
    carrying_capacity = 10000
    params = [calving_interval, pcnt_darted, juvenile_age, max_age, p_calf_survival, p_adult_survival, p_senior_survival, carrying_capacity]

    pop = []
    for i in range( carrying_capacity//4 ):
        # Create a new juvenile or adult male
        pop.append( ['m', random.randint(juvenile_age+1, max_age ) , 0, 0] )
    for i in range( carrying_capacity//4 ):
        # Create a new juvenile or adult female elephant that has been darted
        pop.append( ['f', random.randint(juvenile_age+1, max_age ), 0, random.randint(1,22)] )
    for i in range( carrying_capacity//4 ):
        # Create a new juvenile or adult female elephant that is eligible for pregnancy
        pop.append( ['f', random.randint(juvenile_age+1, max_age ),  0, 0] )
    for i in range( carrying_capacity-3*(carrying_capacity//4) ):
        # Create a new juvenile or adult female elephant that is pregnant
        pop.append( ['f', random.randint(juvenile_age+1, max_age ),  random.randint(1,23), 0] )
    
    # Record the number of elephants that could become pregnant during this
    # second month of simulation. Then we an assess the conception rate.
    numBeforeMonth = len(pop)
    numF = countAdultFemales( params, pop )
    numBreedable = countFemalesEligibleForPregnancy( params, pop )
    pop = elephant.simulateMonth( params, pop )    
    numBabies = len( pop ) - numBeforeMonth
    numNewlyPregnant = countFemalesNewlyPregnant( params, pop )
    print("In month 1, out of %d adult female elephants, %d gave birth, leading to a birth rate of %0.4f. It should be %0.4f" % (numF, numBabies, float(numBabies)/numF,(1/calving_interval)/22))
    print("In month 1, out of %d adult female elephants who could become pregnant, %d became pregnant this month, leading to a conception rate of %0.3f. It should be %0.3f" % (numBreedable, numNewlyPregnant, float(numNewlyPregnant)/numBreedable,1.0/(12*calving_interval-22.0)))
    
    # Take into account darting. The above test is on a populations with no contraceptives. but we also want to test the contraception code. 
    pop = elephant.dartElephants( params, pop )
    
    numF = countAdultFemales( params, pop )
    numBreedable = countFemalesEligibleForPregnancy( params, pop )
    pop = elephant.simulateMonth( params, pop )    
    numNewlyPregnant = countFemalesNewlyPregnant( params, pop )
    print("In month 2, out of %d adult female elephants who could become pregnant, %d became pregnant this month, leading to a conception rate of %0.3f. It should be %0.3f" % (numBreedable, numNewlyPregnant, float(numNewlyPregnant)/numBreedable,1.0/(12*calving_interval-22.0)))
    

if __name__ == '__main__':
    main()
