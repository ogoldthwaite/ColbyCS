#Owen Goldthwaite 
#2/24/19

import data
import numpy as np
import sys
import time
import re
import math
import random
#import scipy.stats as stats
import scipy
import scipy.cluster.vq as vq

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

def pca(dataObj, colHeaders, normalize=True):
    if(normalize):
        A = normalize_columns_seperately(dataObj, colHeaders)
    else:
        A = dataObj.getColVals(colHeaders)

    means = []
    for i in range(A.shape[1]):
        col = (A[:,i])
        means.append(col.mean())
    m = np.matrix(means)

    D = A - m

    U,S,V = np.linalg.svd(D, full_matrices=False)

    eVals = []
    N = A.shape[0]
    for i in range(len(S)):
        eVals.append( (S[i]**2) / (N-1) )
    eigenValues = [eVals]

    projData = (V*D.T).T
    print(colHeaders)
    PCAObj = data.PCAData(projData, V, eigenValues, m, colHeaders)
    return PCAObj

def kmeans_numpy(data, headers, k, whiten=True, useheaders=True):
    if(useheaders == True):
        A = data.getColVals(headers)
    else:
        A = data

    if(whiten):
        W = vq.whiten(A)
    else:
        W = A

    codebook, bookerror = vq.kmeans(W, k)
    codes, error = vq.vq(W, codebook)

    return codebook, codes, error

def kmeans_init(A, K):
    if(A.shape[0] < K):
        print("Less data points than K asks for :)")
        return
    
    matlist = []
    indices = [i for i in range(A.shape[0])]
    random.shuffle(indices)

    for i in range(K):
        matlist.append(A[indices[i], :].tolist()[0])
        print(matlist)

    print(matlist)
    mat = np.matrix(matlist)
    return mat

def kmeans_classify(A, codebook):

    indices = [] #Closest mean to each point
    SSDs = []

    for i in range(A.shape[0]):
        diff = codebook - A[i,:]
        minidx = 0
        mindist = np.sum(np.square(diff[0,:]))
        ssd = mindist
        for row in range(diff.shape[0]):
            curdist = np.sum(np.square(diff[row,:]))
            if(curdist < mindist):
                mindist = curdist
                minidx = row
                ssd = mindist
        indices.append([minidx])
        SSDs.append([ssd])
    
    return np.matrix(indices), np.sqrt(np.matrix(SSDs))

def kmeans_algorithm(A, means, MIN_CHANGE=1e-7, MAX_ITERATIONS=100):
    D = means.shape[1]    # number of dimensions
    K = means.shape[0]    # number of clusters
    N = A.shape[0]        # number of data points

    for i in range(MAX_ITERATIONS):
        codes, errors = kmeans_classify(A, means)
        newmeans = np.zeros_like(means)

        counts = np.zeros((K, 1))

        for j in range(N): #Probably not right :)
            closestmean = codes[j, 0]
            newmeans[closestmean, :] += A[j, :]
            counts[closestmean, 0] += 1 

        for clust in range(K):
            if(not(counts[clust, 0] == 0)):
                newmeans[clust, :] /= counts[clust, 0]
            else:
                newmeans[clust, :] = A[random.randint(0,N), :]

        diff = np.sum(np.square(means-newmeans))
        means = newmeans
        if diff < MIN_CHANGE:
            break

    codes, errors = kmeans_classify(A, means)

    return (means, codes, errors)

def kmeans(data, headers, K, whiten=True):
    A = data.getColVals(headers)
    if(whiten):
        W = vq.whiten(A)
    else:
        W = A
    
    codebook = kmeans_init(W,K)

    codebook, codes, errors = kmeans_algorithm(W, codebook)

    return codebook, codes, errors

def kmeans_quality(errors, K):
    sumval = 0
    print(errors)
    errors = errors.tolist()
    for error in errors:
        sumval += error**2
    sumval += ((K/2)*(np.log2(len(errors))))
    return sumval

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
