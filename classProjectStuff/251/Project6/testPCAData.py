# Bruce A. Maxwell
# Spring 2018
# Updated for python3
# CS 251 Project 6
#
# Test file for the PCAData class
#
import numpy as np
import data

# This is the proper set of eigenvalues and eigenvectors for the small
# data set of four points.
headers = ['A','B']

# original data
orgdata = np.matrix([ [1,2],
                      [2,4],
                      [5,9.5],
                      [4,8.5] ])

# means of the original data
means = np.matrix([ 3.,  6.])

# eigenvalues of the original data
evals = np.matrix([16.13395443, 0.03271224])

# eigenvectors of the original data as rows
evecs = np.matrix([[ 0.4527601,   0.89163238],
                   [-0.89163238,  0.4527601 ]])

# the original data projected onto the eigenvectors.
# pdata = (evecs * (orgdata - means).T).T
pdata = np.matrix([[-4.4720497,  -0.02777563],
                   [-2.23602485, -0.01388782],
                   [ 4.02623351, -0.19860441],
                   [ 2.68184104,  0.24026787]])


# create a PCAData object
pcad = data.PCAData( pdata, evecs, evals, means, headers )

# Test all of the various new functions
print("Eigenvalues:")
print(pcad.get_eigenvalues())

print("\nEigenvectors:")
print(pcad.get_eigenvectors())

print("\nMeans:")
print(pcad.get_original_means())

print("\nOriginal Headers:")
print(pcad.get_original_headers())

# Test old functions
print("\nProjected data:")
print(pcad.getColVals( pcad.getNumericHeaders() ))

print("\nColumn Headers:")
print(pcad.getNumericHeaders())

print("\nColumn Types:")
print(pcad.getTypes())

print("\nNumber of columns:")
print(pcad.getNumDimensions())

print("\nNumber of rows:")
print(pcad.getNumPoints())
