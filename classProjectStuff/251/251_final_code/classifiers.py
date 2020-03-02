# Template by Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

import sys
import data
import math
import analysis as an
import numpy as np
import scipy
import scipy.cluster.vq as vq

class Classifier:

    def __init__(self, type):
        '''The parent Classifier class stores only a single field: the type of
        the classifier.  A string makes the most sense.

        '''
        self._type = type

    def type(self, newtype = None):
        '''Set or get the type with this function'''
        if newtype != None:
            self._type = newtype
        return self._type

    def confusion_matrix( self, truecats, classcats ):
        '''Takes in two Nx1 matrices of zero-index numeric categories and
        computes the confusion matrix. The rows represent true
        categories, and the columns represent the classifier output.
        To get the number of classes, you can use the np.unique
        function to identify the number of unique categories in the
        truecats matrix.
        '''
        unique, mapping = np.unique( np.array(truecats.T), return_inverse=True)

        numClasses = len(unique)

        confmat = np.matrix(np.zeros((numClasses+1, numClasses+1)))
        confmat[0,1:] = unique
        confmat[1:,0] = np.matrix(unique).T


        for row in range(truecats.shape[0]):
            confmat[truecats[row]+1,classcats[row]+1] = confmat[truecats[row]+1,classcats[row]+1] + 1

        return confmat

    def confusion_matrix_str( self, cmtx ):
        '''Takes in a confusion matrix and returns a string suitable for printing.'''
        start = "Confusion Matrix\n\tClassified As\nTruth\n"
        
        line1 = "\t"
        for i in range(cmtx.shape[1]-1):
            line1 += str(int(cmtx[0, i+1])) + "\t"
        
        mat = cmtx[1:, :]
        matstr = ""
        for row in range(mat.shape[0]):
            matstr += "\n"
            for col in range(mat.shape[1]):
                matstr += str(int(mat[row,col])) + "\t"

        datamat = cmtx[1:,1:]
        totalsum = np.sum(datamat)
        correctsum = np.sum(np.diag(datamat))

        acc = f"\n\nPercent Correct: {(correctsum/totalsum)*100}\n"

        s = start + line1 + matstr + acc

        return s

    def __str__(self):
        '''Converts a classifier object to a string.  Prints out the type.'''
        return str(self._type)


class NaiveBayes(Classifier):
    '''NaiveBayes implements a simple NaiveBayes classifier using a
    Gaussian distribution as the pdf.

    '''

    def __init__(self, data=None, headers=[], categories=None, sepcatfile=False):
        '''Takes in a Matrix of data with N points, a set of F headers, and a
        matrix of categories, one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'Naive Bayes Classifier')
        
        # store the headers used for classification
        self.headers = headers
        self.classes = []
        self.numClasses = -1
        self.numFeatures = -1
        self.origClassLabels = []

        # number of classes and number of features
        self.numClasses = None
        self.numFeatures = None
        # if(not(categories is None)):
        #     unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
        #     self.numClasses = len(unique)
            
        # unique data for the Naive Bayes: means, variances, scales, priors
        self.means = None
        self.variances = None
        self.scales = None
        self.priors = None

        # if given data,
            # call the build function
        if(not(data is None)):
            # THIS IS ASSUMING THAT THE FINAL COLUMN OF A DATA FILE IS THE CLASS
            if(sepcatfile):
                self.build(data.getNumericMatrix()[:,:], categories)
            else:
                self.build(data.getNumericMatrix()[:,:-1], categories)
            
    def build( self, A, categories ):
        '''Builds the classifier give the data points in A and the categories
            NOTe FOR MYSELF that this is assuming data doesnt have the categories column anymore :)'''

        if( (A is None) or (categories is None) ):
            print("In NaiveBayes build func either data or categories is None!")
            return

        # figure out how many categories there are and get the mapping (np.unique)
        unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
        self.classes = unique #labels
        self.numClasses = len(unique)
        self.numFeatures = A.shape[1]

        # create the matrices for the means, vars, and scales
        self.classMeans = None
        self.classVars = None
        self.classScales = None
        self.classPriors = []

        # the output matrices will be of thr shape categoriesxfeatures
        # compute the means/vars/scales/priors for each class
        means = []
        variances = []
        scales = []
        for cat in range(self.numClasses):
            curdata = A[mapping==cat, :]
            # means
            curmeans = np.mean(curdata, axis=0)
            means.append(curmeans.tolist()[0])
            # variances
            curvars = np.var(curdata, axis=0, ddof=1)
            variances.append(curvars.tolist()[0])
            #scales
            curscales = []
            for var in curvars.tolist()[0]:
                curscales.append(1 / math.sqrt((2*math.pi) * var))
            scales.append(curscales)
            #priors
            numberofclass = curdata.shape[0]
            totalnumber = A.shape[0]
            self.classPriors.append(numberofclass / totalnumber)

        self.classMeans = np.matrix(means)
        self.classVars = np.matrix(variances)
        self.classScales = np.matrix(scales)

        # the prior for class i will be the number of examples in class i divided by the total number of examples
        
        # store any other necessary information: # of classes, # of features, original labels

        return

    def classify( self, A, return_likelihoods=False ):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_likelihoods
        is True, it also returns the probability value for each class, which
        is product of the probability of the data given the class P(Data | Class)
        and the prior P(Class).

        '''
        # error check to see if A has the same number of columns as the class means
        if(not(A.shape[1] == self.classMeans.shape[1])):
            print("Data A does not have the same number of columns as class means, should be a mean for each column!")
            return

        # make a matrix that is N x C to store the probability of each class for each data point
        P = np.matrix(np.zeros((A.shape[0], self.numClasses))) # a matrix of zeros that is N (rows of A) x C (number of classes)

        # Calcuate P(D | C) by looping over the classes
        #  with numpy-fu you can do this in one line inside a for
        #  loop, calculating a column of P in each loop.
        #
        #  To compute the likelihood, use the formula for the Gaussian
        #  pdf for each feature, then multiply the likelihood for all
        #  the features together The result should be an N x 1 column
        #  matrix that gets assigned to a column of P
        for cat in range(self.numClasses):
            mean = self.classMeans
            var = self.classVars
            scale = self.classScales
            prior = self.classPriors[cat]
            
            data = A

            P[:,cat] = np.multiply(np.prod( np.multiply( np.exp(-( np.square(data-mean[cat]) / (2*((var[cat]))) )), scale[cat] ), axis=1 ), prior)

        # calculate the most likely class for each data point
        cats = np.argmax(P, axis=1) # take the argmax of P along axis 1
        # use the class ID as a lookup to generate the original labels
        labels = self.classes[cats]

        if return_likelihoods:
            return cats, labels, P

        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nNaive Bayes Classifier\n"
        for i in range(self.numClasses):
            s += 'Class %d --------------------\n' % (i)
            s += 'Mean  : ' + str(self.classMeans[i,:]) + "\n"
            s += 'Var   : ' + str(self.classVars[i,:]) + "\n"
            s += 'Scales: ' + str(self.classScales[i,:]) + "\n"
            s += 'Prior: '  + str(self.classPriors[i]) + "\n"

        s += "\n"
        return s
        
    def write(self, filename):
        '''Writes the Bayes classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the Bayes classifier from the file'''
        # extension
        return

    
class KNN(Classifier):

    def __init__(self, data=None, headers=[], categories=None, K=None, sepcatfile=False):
        '''Take in a Matrix of data with N points, a set of F headers, and a
        matrix of categories, with one category label for each data point.'''

        # call the parent init with the type
        Classifier.__init__(self, 'KNN Classifier')
        
        # store the headers used for classification
        self.headers = headers

        # number of classes and number of features
        self.classes = None
        self.numClasses = None
        self.numFeatures = None

        # original class labels, self.classes

        # unique data for the KNN classifier: list of exemplars (matrices)
        self.exemplars = []
        # if given data,
            # call the build function
        if(not(data is None)):
            if(sepcatfile):
                self.build(data.getNumericMatrix()[:,:], categories)
            else: 
                self.build(data.getNumericMatrix()[:,:-1], categories)


    def build( self, A, categories, K = None ):
        '''Builds the classifier give the data points in A and the categories'''

        if( (A is None) or (categories is None) ):
            print("In KNN build func either data or categories is None!")
            return

        # figure out how many categories there are and get the mapping (np.unique)
        unique, mapping = np.unique( np.array(categories.T), return_inverse=True)
        self.classes = unique #labels
        self.numClasses = len(unique)
        self.numFeatures = A.shape[1]
        print(unique)

        # for each category i, build the set of exemplars
        for cat in range(self.numClasses):
            # if K is None
            if K == None:
                # append to exemplars a matrix with all of the rows of A where the category/mapping is i
                self.exemplars.append(A[mapping==cat, :])
            # else
            else:
                # run K-means on the rows of A where the category/mapping is i
                codebook, bookerror = vq.kmeans(A[mapping==cat, :], K)
                # append the codebook to the exemplars
                self.exemplars.append(codebook)

        # store any other necessary information: # of classes, # of features, original labels

        return

    def classify(self, A, return_distances=False, K=3):
        '''Classify each row of A into one category. Return a matrix of
        category IDs in the range [0..C-1], and an array of class
        labels using the original label values. If return_distances is
        True, it also returns the NxC distance matrix. The distance is 
        calculated using the nearest K neighbors.'''

        # error check to see if A has the same number of columns as the class means
        if(not(A.shape[1] == self.numFeatures)):
            print("Data A does not have the same number of columns as class means, should be a mean for each column!")
            return

        # make a matrix that is N x C to store the distance to each class for each data point
        D = np.matrix(np.zeros((A.shape[0], self.numClasses))) # a matrix of zeros that is N (rows of A) x C (number of classes)
        # for each class i
        for cat in range(self.numClasses):
            # make a temporary matrix that is N x M where M is the number of examplars (rows in exemplars[i])
            exemplars = self.exemplars[cat]
            # calculate the distance from each point in A to each point in exemplar matrix i (for loop)
            for row in range(A.shape[0]):
                currow = A[row,:]
                distance = np.sum(np.sort(np.sqrt(np.sum(np.square(exemplars - currow), axis=1)) ,axis=0)[:K])

                D[row, cat] = distance
            # sort the distances by row
            # sum the first K columns
            # this is the distance to the first class

        # calculate the most likely class for each data point
        cats = np.nanargmin(D, axis=1) # take the argmin of D along axis 1

        # use the class ID as a lookup to generate the original labels
        labels = self.classes[cats]

        if return_distances:
            return cats, labels, D

        return cats, labels

    def __str__(self):
        '''Make a pretty string that prints out the classifier information.'''
        s = "\nKNN Classifier\n"
        for i in range(self.numClasses):
            s += 'Class %d --------------------\n' % (i)
            s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
            s += 'Mean of Exemplars  :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

        s += "\n"
        return s


    def write(self, filename):
        '''Writes the KNN classifier to a file.'''
        # extension
        return

    def read(self, filename):
        '''Reads in the KNN classifier from the file'''
        # extension
        return
    

# test function
def main(argv):
    # test function here
    if len(argv) < 3:
        print( 'Usage: python %s <training data file> <test data file> <optional training categories file> <optional test categories file>' % (argv[0]) )
        print( '    If categories are not provided as separate files, then the last column is assumed to be the category.')
        exit(-1)

    train_file = argv[1]
    test_file = argv[2]
    dtrain = data.Data(train_file)
    dtest = data.Data(test_file)


    if len(argv) >= 5:
        train_headers = dtrain.getNumericHeaders()
        test_headers = dtrain.getNumericHeaders()
        
        traincat_file = argv[3]
        testcat_file = argv[4]

        traincats = data.Data(traincat_file)
        traincatdata = traincats.getColVals(traincats.getNumericHeaders())

        testcats = data.Data(testcat_file)
        testcatdata = testcats.getColVals(testcats.getNumericHeaders())

    else:
        train_headers = dtrain.getNumericHeaders()[:-1]
        test_headers = dtrain.getNumericHeaders()[:-1]

        traincatdata = dtrain.getColVals([dtrain.getNumericHeaders()[-1]])
        testcatdata = dtest.getColVals([dtest.getNumericHeaders()[-1]])

    
    nbc = NaiveBayes(dtrain, train_headers, traincatdata, sepcatfile=True )

    print( 'Naive Bayes Training Set Results' )
    A = dtrain.getColVals(train_headers)
    
    newcats, newlabels, p = nbc.classify( A, return_likelihoods=True )


    uniquelabels, correctedtraincats = np.unique( traincatdata.T.tolist()[0], return_inverse = True)
    correctedtraincats = np.matrix([correctedtraincats]).T

    confmtx = nbc.confusion_matrix( correctedtraincats, newcats )
    print( nbc.confusion_matrix_str( confmtx ) )


    print( 'Naive Bayes Test Set Results' )
    A = dtest.getColVals(test_headers)
    
    newcats, newlabels = nbc.classify( A )

    uniquelabels, correctedtestcats = np.unique( testcatdata.T.tolist()[0], return_inverse = True)
    correctedtestcats = np.matrix([correctedtestcats]).T

    confmtx = nbc.confusion_matrix( correctedtestcats, newcats )
    print( nbc.confusion_matrix_str( confmtx ) )

    print( '-----------------' )
    print( 'Building KNN Classifier' )
    knnc = KNN( dtrain, train_headers, traincatdata, 10, sepcatfile=True )

    print( 'KNN Training Set Results' )
    A = dtrain.getColVals(train_headers)

    newcats, newlabels = knnc.classify( A )

    confmtx = knnc.confusion_matrix( correctedtraincats, newcats )
    print( knnc.confusion_matrix_str(confmtx) )

    print( 'KNN Test Set Results' )
    A = dtest.getColVals(test_headers)

    newcats, newlabels = knnc.classify(A)

    # print the confusion matrix
    confmtx = knnc.confusion_matrix( correctedtestcats, newcats )
    print( knnc.confusion_matrix_str(confmtx) )

    return
    
if __name__ == "__main__":
    main(sys.argv)