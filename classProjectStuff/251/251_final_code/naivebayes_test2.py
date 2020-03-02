# Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Naive Bayes class test
#

import sys
import data
import classifiers

def main(argv):

    if len(argv) < 3:
        print( 'Usage: python %s <train data file> <test data file> <optional train categories> <optional test categories>' % (argv[0]) )
        exit(-1)
        
    dtrain = data.Data(argv[1])
    dtest = data.Data(argv[2])

    if len(argv) > 3:
        traincatdata = data.Data(argv[3])
        trainlabels = traincatdata.getColVals( [traincatdata.getNumericHeaders()[0]] )
        testcatdata = data.Data(argv[4])
        testlabels = testcatdata.getColVals( [testcatdata.getNumericHeaders()[0]] )
        A = dtrain.getColVals( dtrain.getNumericHeaders() )
        B = dtest.getColVals( dtest.getNumericHeaders() )
        
    else:
        # assume the categories are the last column
        trainlabels = dtrain.getColVals( [dtrain.getNumericHeaders()[-1]] )
        testlabels = dtest.getColVals( [dtest.getNumericHeaders()[-1]] )
        A = dtrain.getColVals( dtrain.getNumericHeaders()[:-1] )
        B = dtest.getColVals( dtest.getNumericHeaders()[:-1] )
        

    # create a new classifier
    nbc = classifiers.NaiveBayes()

    # build the classifier using the training data
    nbc.build( A, trainlabels )

    # use the classifier on the training data
    ctraincats, ctrainlabels, P = nbc.classify( A, return_likelihoods=True )
    ctestcats, ctestlabels = nbc.classify( B )

    print( 'Results on Training Set:' )
    print( '     True  Est' )
    for i in range(ctrainlabels.shape[0]):
        if int(trainlabels[i,0]) == int(ctrainlabels[i,0]):
            print( "%03d: %4d %4d" % (i, int(trainlabels[i,0]), int(ctrainlabels[i,0]) ) )
        else:
            print( "%03d: %4d %4d **" % (i, int(trainlabels[i,0]), int(ctrainlabels[i,0]) ) )
            
    print( 'P matrix for Training Set:' )
    print( P )

    print( 'Results on Test Set:' )
    print( '     True  Est' )
    for i in range(ctestlabels.shape[0]):
        if int(testlabels[i,0]) == int(ctestlabels[i,0]):
            print( "%03d: %4d %4d" % (i, int(testlabels[i,0]), int(ctestlabels[i,0]) ) )
        else:
            print( "%03d: %4d %4d **" % (i, int(testlabels[i,0]), int(ctestlabels[i,0]) ) )
    return

if __name__ == "__main__":
    main(sys.argv)
        