#Just splits the csv into a 70 / 30 split for training and testing
import sys
import random

def splitfile(filename, trainoutname, testoutname, trainperc=.7):
    inputfile = open(filename, "r")
    trainfile = open(trainoutname, "w")
    testfile = open(testoutname, "w")

    
    inputstr = inputfile.readlines()
    
    trainfile.write(inputstr[0])
    trainfile.write(inputstr[1])
    testfile.write(inputstr[0])
    testfile.write(inputstr[1])

    inputstr = inputstr[2:]


    for line in inputstr:
        choice = random.random()
        if(choice < trainperc):
            trainfile.write(line)
        else:
            testfile.write(line)

    inputfile.close()
    trainfile.close()
    testfile.close()



def main(argv):
    if(len(argv) < 5):
        print("Usage:python splitcsv.py <input filename> <new train out name> <new test out name> <split percentage")
        exit(-1)
    
    try:
        if(float(argv[4]) > 1.0):
            argv[4] = 1.0
    except ValueError:
        print("Please enter a valid float thats <=1 for the split percentage")
        exit(-1)
    
    splitfile(argv[1], argv[2], argv[3], trainperc=float(argv[4]))




if __name__ == "__main__":
    main(sys.argv)