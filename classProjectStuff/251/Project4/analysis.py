#Owen Goldthwaite 
#2/24/19

import data
import numpy as np
import sys
import time
import re
import math

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


def main(argv):
    # test command line arguments
    if len(argv) < 3:
        print( 'Usage: python %s <csv filename> <1 for defined types in metadata, 0 for no>' % (argv[0]))
        print( 'By defined types I mean when it says numeric or string etc. in the second 2 ')
        exit(0)

    # create a data object, which reads in the data
    dobj = data.Data(argv[1], argv[2])

    # print out information about the dat
    print('Number of rows:    ', dobj.getNumPoints() )
    print('Number of columns: ', dobj.getNumDimensions() )

    # print out the headers
    print("\nHeaders:")
    headers = dobj.getNumericHeaders()
    s = headers[0]
    for header in headers[1:]:
        s += ", " + header
    print( s )


    print(dobj.getNumericMatrix())

    print("\nData Ranges:")
    print(data_range(dobj, headers))

    print("\nMeans:")
    print(mean(dobj, headers))

    print("\nStandard Dev:")
    print(stdev(dobj, headers),"\n")

    print("\nTesting addColumn()")
    col1 = [i for i in range(dobj.getNumPoints())]
    col2 = []
    for i in range(dobj.getNumPoints()):
        col2.append('new col')
    
    print("\nHeaders before any columns are added")
    print(dobj.getRawHeaders())
    print("\nRaw Data Matrix before columns have been added")
    print(dobj.getRawMatrix())

    dobj.addColumn("new numbers", "numeric", col1)
    dobj.addColumn("new strings", "string", col2)
   
    print("\nHeaders after any columns are added")
    print(dobj.getRawHeaders())
    print("\nRaw Data Matrix after columns have been added")
    print(dobj.getRawMatrix())

    print("\nRaw Header to Column Dictionary after Column Additions")
    print(dobj.raw_headercol)

    print("\nNormalized Seperately:")
    print(normalize_columns_seperately(dobj, headers))

    print("\nNormalized Together:")
    print(normalize_columns_together(dobj, headers))

if __name__ == "__main__":
    main(sys.argv)
