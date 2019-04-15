# Owen Goldthwaite
# Fall 2017
# CS 152 Project 7
#
# First class design
#
# Elephant class

import random

# define an Elephant class that holds all necessary information about an elephant
class Elephant:

    # global fixed properties of elephants
    # assign JuvenileAge, MaxAge as constants here
    JuvenileAge = 12
    MaxAge = 60

    # init function 
    def __init__(self, calvingInterval = 3.1, age=None):

        if(age != None):
            self.age = age
        else:
            self.age = random.randint(1, Elephant.MaxAge)

        if(random.random() < .5):
            self.gender = 'f'
        else:
            self.gender = 'm'
        
        self.pregnant = 0
        self.contraception = 0

        if(self.gender == 'f') and (self.age >= 12):
            if(random.random() < (1.0/calvingInterval)):
                self.pregnant = random.randint(1,22)
                
        return        
    
    #Gets
    def getGender(self):
        return self.gender
    
    def getMonthsPregnant(self):
        return self.pregnant
    
    def getContraception(self):
        return self.contraception
    
    def getAge(self):
        return self.age
    
    #Booleans
    def isPregnant(self):
        return self.pregnant > 0
    
    def isCalf(self):
        return self.age <= 1
        
    def isJuvenile(self):
        return self.age <= 12 and self.age > 1
    
    def isAdult(self):
        return self.age <= 60 and self.age > 12
    
    def isSenior(self):
        return self.age > 60
    
    def isFemale(self):
        return self.gender == 'f'


    # Set functions for age, gender, months pregnant, contraception.
    def setGender(self, gender):
        self.gender = gender
        pass

    def setMonthsPregnant(self, mPreg):
        self.pregnant = mPreg
        pass

    def setContraception(self, mContra):
        self.contraception = mContra
        pass

    def setAge(self, a):
        self.age = a
        pass


    def incrementAge(self):
        self.age += 1   
        pass

    def dart(self, monthsEffective = 22):
        # set self.pregnant to 0 and self.contraception to
        # monthsEffective.
        self.pregnant = 0
        self.contraception = monthsEffective
        
        pass

    # Makes an elephant one month older by modifying self.contraception or self.pregnant appropriately
    # returns True if a baby should be created, False otherwise
    
    #May not currently work! Email someone!
    def progressMonth(self, calvingInterval):

        if(self.isFemale() and self.isAdult()):
            if(self.contraception > 0):
                self.contraception -= 1
            elif(self.pregnant > 0 and self.contraception == 0):
                if(self.pregnant >= 22):
                    self.pregnant = 0
                    return True
                else:
                    self.pregnant += 1      
            else:
                if(random.random() < (1.0/(calvingInterval*12 - 22))):
                    self.pregnant = 1
        
        return False
        

    # function that returns a string appropriate for printing
    def __str__(self):
        s = "Age: %2d  Sex: %s" % (self.age, self.gender)
        if self.isFemale() and self.contraception > 0:
            s += "  Contraception: %d" % (self.contraception)
        elif self.gender == 'f' and self.pregnant > 0:
            s += "  Pregnant: %d" % (self.pregnant)

        return s

# test function that makes 20 elephants and prints them out
def test():
    print("Making 20 elephants")
    random.seed(3)
    for i in range(20):
        # Make an Elephant object and store in the the variable e
        e = Elephant()
        print(e)
        #e.progressMonth(3.1)   
        print(e)
        print("MP: ", e.getMonthsPregnant())
#         print( "isFemale: ", e.isFemale() )
#         print( "set age to ", e.getMonthsPregnant() )           
        

if __name__ == "__main__":
    test()
