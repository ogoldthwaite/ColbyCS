# Bruce A. Maxwell
# Spring 2018
# Updated for python3
# CS 251 Project 6
#
# PCA test function
#
import numpy as np
import data
import analysis
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python %s <data file>' % (sys.argv[0]))
        exit()

    data = data.Data( sys.argv[1] )
    pcadata = analysis.pca( data, data.getNumericHeaders(), False )

    print("\nOriginal Data Headers")
    print(pcadata.getOriginalHeaders())
    print("\nOriginal Data" )
    print(data.getColVals( data.getNumericHeaders() ))
    print("\nOriginal Data Means")
    print(pcadata.getOriginalMeans())
    print("\nEigenvalues")
    print(pcadata.getEigenvalues())
    print("\nEigenvectors")
    print(pcadata.getEigenvectors())
    print("\nProjected Data")
    print(pcadata.getColVals(pcadata.getNumericHeaders()))
    print("\nPCA Headers")
    print(pcadata.getNumericHeaders())
