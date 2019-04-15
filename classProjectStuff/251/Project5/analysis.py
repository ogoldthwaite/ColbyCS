#Owen Goldthwaite 
#2/24/19

import data
import numpy as np
import sys
import time
import re
import math
import scipy.stats as stats

def data_range(data, col_headers):
    matrix = data.getColVals(col_headers)
    returnlist = []
    for i in range(matrix.shape[1]):
        col = (matrix[:,i])
        returnlist.append([col.min(), col.max()])
    
    return returnlist

def mean(data, col_headers):
    matrix = data.getColVals(col_headers)
    returnlist = []
    for i in range(matrix.shape[1]):
        col = (matrix[:,i])
        returnlist.append(col.mean())
    
    return returnlist

def stdev(data, col_headers):
    matrix = data.getColVals(col_headers)
    returnlist = []
    for i in range(matrix.shape[1]):
        col = (matrix[:,i])
        returnlist.append(col.std())
    
    return returnlist

def normalize_columns_seperately(data, col_headers):
    matrix = data.getColVals(col_headers)
    return (matrix - matrix.min(axis=0)) / (matrix.max(axis=0) - matrix.min(axis=0))

def normalize_columns_together(data, col_headers):
    matrix = data.getColVals(col_headers)
    return (matrix - matrix.min()) / (matrix.max() - matrix.min())

# indieVar and dependVar are header names I'm assuming
def single_linear_regression(data, indieVar, dependVar):
    indieCol = data.getColVals(indieVar, singleheader=True).tolist()
    dependCol = data.getColVals(dependVar, singleheader=True).tolist()
    (minIndie, maxIndie) = min(indieCol)[0], max(indieCol)[0]
    (minDepend, maxDepend) = min(dependCol)[0], max(dependCol)[0]

    slope, yInt, rVal, pVal, stderr = stats.mstats.linregress(indieCol,dependCol)
    regressTupe = (slope, yInt, rVal, pVal, stderr)
    return regressTupe, (minIndie, maxIndie), (minDepend, maxDepend)


def linear_regression(data, indieHeaders, dependHeader):
    y = data.getColVals(dependHeader, singleheader=True)
    # Potentially may have to check if indieHeaders is longer than 1 item
    A = data.getColVals(indieHeaders)
    A = np.hstack((A, np.ones((A.shape[0], 1))))

    AAinv = np.linalg.inv(np.dot(A.T, A))

    x = np.linalg.lstsq(A, y)

    b = x[0]
    N = y.shape[0]
    C = b.shape[0]
    df_e = N-C
    df_r = C-1

    error = y - np.dot(A,b)
    sse = np.dot(error.T, error) / df_e
    stderr = np.sqrt(np.diagonal(sse[0,0] * AAinv))

    t = b.T / stderr

    p = 2*(1-stats.t.cdf(abs(t), df_e))

    r2 = 1-error.var() / y.var()

    return b, sse, r2, t, p

def test(filename):
    d = data.Data(filename)
    b, sse, r2, t, p = linear_regression(d, ['DLY-TMIN-NORMAL', 'DLY-TMAX-NORMAL'], 'DLY-TAVG-NORMAL')
    print("m0: ", b[0,0])
    print("m1: ", b[1,0])
    print("b: ", b[2,0])
    print("sse: ", sse)
    print("r2: ", r2)
    print("t: ", t)
    print("p: ", p)


def main(argv):
    # test command line arguments
    if len(argv) < 2:
        print( 'Usage: python %s <csv filename>')
        exit(0)

    test(argv[1])



if __name__ == "__main__":
    main(sys.argv)
