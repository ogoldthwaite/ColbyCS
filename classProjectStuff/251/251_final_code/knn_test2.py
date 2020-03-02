# Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# KNN class test
#

import sys
import data
import classifiers

def main(argv):
    '''Reads in a training set and a test set and builds two KNN
    classifiers.  One uses all of the data, one uses 10
    exemplars. Then it classifies the test data and prints out the
    results.
    '''

    # usage
    if len(argv) < 3:
        print( 'Usage: python %s <training data file> <test data file> <optional training category file> <optional test category file>' % (argv[0]) )
        exit(-1)

    # read the training and test sets
    dtrain = data.Data(argv[1])
    dtest = data.Data(argv[2])

    # get the categories and the training data A and the test data B
    if len(argv) > 4:
        traincatdata = data.Data(argv[3])
        testcatdata = data.Data(argv[4])
        traincats = traincatdata.getColVals( [traincatdata.getNumericHeaders()[0]] )
        testcats = testcatdata.getColVals( [testcatdata.getNumericHeaders()[0]] )
        A = dtrain.getColVals( dtrain.getNumericHeaders() )
        B = dtest.getColVals( dtest.getNumericHeaders() )
    else:
        # assume the categories are the last column
        traincats = dtrain.getColVals( [dtrain.getNumericHeaders()[-1]] )
        testcats = dtest.getColVals( [dtest.getNumericHeaders()[-1]] )
        A = dtrain.getColVals( dtrain.getNumericHeaders()[:-1] )
        B = dtest.getColVals( dtest.getNumericHeaders()[:-1] )

    # create two classifiers, one using 10 exemplars per class
    knncall = classifiers.KNN()
    knnc10 = classifiers.KNN()

    # build the classifiers
    knncall.build( A, traincats )
    knnc10.build(A, traincats, 10)

    # use the classifiers on the test data
    allcats, alllabels = knncall.classify( B )

    tencats, tenlabels = knnc10.classify( B )

    # print the results
    print( 'Results using All Exemplars:' )
    print( '     True  Est' )
    for i in range(allcats.shape[0]):
        if int(testcats[i,0]) == int(alllabels[i,0]):
            print( "%03d: %4d %4d" % (i, int(testcats[i,0]), int(alllabels[i,0]) ) )
        else:
            print( "%03d: %4d %4d **" % (i, int(testcats[i,0]), int(alllabels[i,0]) ) )

    print( knnc10 )

    print( 'Results using 10 Exemplars:' )
    print( '     True  Est' )
    for i in range(tencats.shape[0]):
        if int(testcats[i,0]) == int(tenlabels[i,0]):
            print( "%03d: %4d %4d" % (i, int(testcats[i,0]), int(tenlabels[i,0]) ) )
        else:
            print( "%03d: %4d %4d **" % (i, int(testcats[i,0]), int(tenlabels[i,0]) ) )

    return

if __name__ == "__main__":
    main(sys.argv)