import sys
import data
import numpy as np
import classifiers


def classify(trainfile, testfile, trainlabels=None, testlabels=None, classtype='KNN', outputfile="classifyoutput.csv"):
    dtrain = data.Data(trainfile)
    dtest = data.Data(testfile)

    # get the categories and the training data A and the test data B
    if(not(trainlabels == None)):
        traincatdata = data.Data(trainlabels)
        testcatdata = data.Data(testlabels)
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

    if classtype == 'KNN':
        classifier = classifiers.KNN()
        classifier.build(A, traincats)
    elif classtype == 'Bayes':
        classifier = classifiers.NaiveBayes()
        classifier.build(A, traincats)
    else:
        print("In classify function, not a valid classification style")
        return

    print(f"\nTrain Data Matrix: Classifier type: {classtype}\n")

    newcats, newlabels = classifier.classify( A )

    uniquelabels, correctedtraincats = np.unique( traincats.T.tolist()[0], return_inverse = True)
    correctedtraincats = np.matrix([correctedtraincats]).T

    confmtx = classifier.confusion_matrix( correctedtraincats, newcats )
    print( classifier.confusion_matrix_str( confmtx ) )

    
    print(f"\nTest Data Matrix: Classifier type: {classtype}\n")

    newcats, newlabels = classifier.classify( B )

    uniquelabels, correctedtestcats = np.unique( testcats.T.tolist()[0], return_inverse = True)
    correctedtestcats = np.matrix([correctedtestcats]).T

    confmtx = classifier.confusion_matrix( correctedtestcats, newcats )
    print( classifier.confusion_matrix_str( confmtx ) )

    newcol = []
    for row in range(newcats.shape[0]):
        newcol.append(newcats[row,0])
    
    dtest.addColumn("pred_class","numeric",newcol)
    dtest.write(outputfile, dtest.getNumericHeaders())

    return



def main(argv):
    
    if len(argv) < 4:
        print( 'Usage: python %s <training data file> <test data file> <classifier type KNN or Bayes> <optional training category file> <optional test category file> ' % (argv[0]) )
        exit(-1)

    filename = input("Enter output file name: \n")

    if(len(argv) > 4):
        classify(argv[1], argv[2], trainlabels=argv[4], testlabels=argv[5], classtype=argv[3], outputfile=filename)
    else:
        classify(argv[1], argv[2], classtype=argv[3], outputfile=filename)



if __name__ == "__main__":
    main(sys.argv)    