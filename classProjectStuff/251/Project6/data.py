#Owen Goldthwaite 
#2/20/19

import numpy as np
import time
import re
import analysis
import sys
import csv

class Data:
	def __init__(self, filename = None, definedtypes=True, headerlist = None, matrix = None):
		self.filename = filename
		self.raw_headerlist = headerlist
		self.datatypes = []
		self.numeric_matrix = matrix #Should be numpy matrix
		self.raw_matrix = matrix
		self.numeric_headercol = {} #maps a header to it's corresponding column of values
		self.raw_headercol = {}
		
		if(definedtypes == True or definedtypes == "1"):
			self.defined_types = True
		else:
			self.defined_types = False

		if self.filename is not None:
			self.read(filename)
		else:
			self.numeric_headerlist = headerlist

	# Reads one of 4 date string formats and convert to float time value, return that float. Throws value error on no match
	def readDates(self, date):
		r1 = re.compile("^\d{1,2}\/\d{1,2}\/\d{4}$")
		r2 = re.compile("^\d{1,2}\/\d{1,2}\/\d{2}$")
		r3 = re.compile("^\d{1,2}\ \d{1,2}\ \d{4}$")
		r4 = re.compile("^\d{1,2}\ \d{1,2}\ \d{2}$")

		timestruct = None
		if(r1.match(date)is not None):
			timestruct = time.strptime(date, "%m/%d/%Y")
		elif(r2.match(date)is not None):
			timestruct = time.strptime(date, "%m/%d/%y")
		elif(r3.match(date)is not None):
			timestruct = time.strptime(date, "%m %d %Y")
		elif(r4.match(date)is not None):
			timestruct = time.strptime(date, "%m/%d/%y")
		else:
			return ValueError
		
		return time.mktime(timestruct)

	
	def read(self, filename):
		fptr = open(filename, mode='rU')
		csv_reader = csv.reader(fptr)

		self.raw_headerlist = [word.strip() for word in next(csv_reader)]
		self.numeric_headerlist = self.raw_headerlist[:]
		numeric_cols = []
		nonnumeric_cols = []
		
		
		if(self.defined_types == True):
			self.datatypes = [word.strip() for word in next(csv_reader)]
			
			# parsing headerlist and datatypes to decide where numeric and nonnumeric columns are
			# only works if file specifies data types
			for i in range(len(self.datatypes)):					
				if( (self.datatypes[i] == "numeric") or (self.datatypes[i] == "date")):
					numeric_cols.append(i)
				else:
					nonnumeric_cols.append(i)
			# method for when types are specified
			numeric_data = []
			raw_data = []

			for line in csv_reader:
				numeric_line = [line[j] for j in numeric_cols]
				numeric_subdata = []
				for i in numeric_line:		
					try: 
						numeric_subdata.append(float(i))
					except ValueError:
						try:
							numeric_subdata.append(self.readDates(i))
						except ValueError:
							continue

				raw_subdata = [i for i in line]
				numeric_data.append(numeric_subdata)
				raw_data.append(raw_subdata)	
			self.numeric_matrix = np.matrix(numeric_data)
			self.raw_matrix = np.matrix(raw_data)
		else:				
			# creating numpy matrix of only numeric data, this method words when types are not specified
			numeric_data = []
			raw_data = []
			first = True
			for line in csv_reader:
				numeric_subdata = []
				raw_subdata = []
				for item in line:
					raw_subdata.append(item)
					try:
						numeric_subdata.append(float(item))
						if(first):
							numeric_cols.append(line.index(item))
					except ValueError:
						if(first):
							nonnumeric_cols.append(line.index(item))	
										
				first = False
				numeric_data.append(numeric_subdata)
				raw_data.append(raw_subdata)
			self.numeric_matrix = np.matrix(numeric_data)
			self.raw_matrix = np.matrix(raw_data)

		# removing non-numeric column headers from headerlist
		for i in nonnumeric_cols:
			del self.numeric_headerlist[i]
			nonnumeric_cols[:] = [x - 1 for x in nonnumeric_cols]
		
		for index, header in enumerate(self.numeric_headerlist):		
			self.numeric_headercol[header] = index

		for index, header in enumerate(self.raw_headerlist):		
			self.raw_headercol[header] = index

		

	# returns the parts of the matrix specified by given list of column headers and row indexes
	# currently uses strings for column headers not indexes, not sure which one we're supposed to use!
	# getDat()
	def getColVals(self, colheaders, rowIndexes=[], singleheader=False):
		first = True
		data = []
		if(singleheader):		
			colheaders = [colheaders]
		for header in colheaders:
			if(header in self.numeric_headerlist):
				for i in range(self.getNumDimensions()):
					curVal = self.getValue(header, i)
					if(isinstance(curVal, (list,))):
						data.append(curVal[self.numeric_headercol[header]])
					else:
						data = [[self.getValue(header, i)] for i in range(self.getNumPoints())]
						break

				if(first):
					col_matrix = np.matrix(data)
					first = False
				else:
					col_matrix = np.hstack((col_matrix, data))
		
		return col_matrix

	def addColumn(self, header, dtype, column):
		if(not (len(column) == self.getNumPoints()) ):
			print(f"addColumn(): Size of column {column} not valid")
			return
		
		raw_data = []
		numeric_data = []
		if(not(self.defined_types)):
			nan_found = False
			for item in column:
				raw_data.append([item])
				try:
					numeric_data.append([float(item)])
				except ValueError:
					nan_found = True
			
			self.raw_headercol[header] = len(self.raw_headerlist)
			self.raw_headerlist.append(header)
			if(not(nan_found)):
				self.numeric_headercol[header] = len(self.numeric_headerlist)
				self.numeric_headerlist.append(header)
				self.numeric_matrix = np.hstack((self.numeric_matrix, numeric_data))					
		else:
			self.raw_headercol[header] = len(self.raw_headerlist)
			self.raw_headerlist.append(header)
			raw_data = [[item] for item in column]
			
			if(dtype == 'numeric'):
				self.datatypes.append(dtype)
				self.numeric_headercol[header] = len(self.numeric_headerlist)
				self.numeric_headerlist.append(header)
				numeric_data = [[float(item)] for item in column]
				self.numeric_matrix = np.hstack((self.numeric_matrix, numeric_data))

		self.raw_matrix = np.hstack((self.raw_matrix, raw_data))

	def getRawHeaders(self):
		return self.raw_headerlist

	def getNumericHeaders(self):
		return self.numeric_headerlist

	def getTypes(self):
		if(self.datatypes == []):
			self.datatypes = [type(i) for i in self.numeric_matrix[0, :].tolist()[0]]
		return self.datatypes

	# returns columns of numeric matrix
	def getNumDimensions(self):
		return self.numeric_matrix.shape[1] #shapes returns tuple (rows, cols)

	# returns rows of numeric matrix
	def getNumPoints(self):
		return self.numeric_matrix.shape[0]

	def getRow(self, rowIndex):
		return self.numeric_matrix[rowIndex, :]

	#returns value in column of header at rowIndex
	def getValue(self, header, rowIndex): 
		return self.numeric_matrix[rowIndex, self.numeric_headercol[header]]

	def getRawValue(self, header, rowIndex): 
		return self.raw_matrix[rowIndex, self.raw_headercol[header]]

	def getNumericMatrix(self):
		return self.numeric_matrix

	def getRawMatrix(self):
		return self.raw_matrix
	#This may not work also change it so it looks nicer maybe	
	def __str__(self):
		return self.numeric_matrix.__str__()

class PCAData(Data):
	def __init__(self, matrix = None, eVecs = None, eVals = None, meanVals = None, headerlist = None):
		self.eVals = eVals
		self.eVecs = eVecs
		self.meanVals = meanVals
		self.origHeaderlist = headerlist

		self.PCAHeaders = []
		for i in range(len(self.origHeaderlist)):
			self.PCAHeaders.append( "PCA" + str(i) )

		Data.__init__(self, headerlist=self.PCAHeaders, matrix=matrix)		

		for index, header in enumerate(self.PCAHeaders):
			self.numeric_headercol[header] = index
			
		self.headercol = self.numeric_headercol

	def getEigenvalues(self):
		return self.eVals

	def getEigenvectors(self):
		return self.eVecs

	def getOriginalMeans(self):
		return self.meanVals

	def getOriginalHeaders(self):
		return self.origHeaderlist


def main(argv):
    # test command line arguments
    if len(argv) < 2:
        print( 'Usage: python %s <csv filename>' % (argv[0]))
        exit(0)

    # create a data object, which reads in the data
    dobj = Data(argv[1])

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

    # print out the types
    print("\nTypes")
    types = dobj.getTypes()
    s = types[0]
    for type in types[1:]:
        s += ", " + type
    print( s )

    # print out a single row
    print("\nPrinting row index 2")
    print( dobj.getRow( 2 ) )

    # print out all of the data
    print("\nData")
    headers = dobj.getNumericHeaders()
    for i in range(dobj.getNumPoints()):
        print(headers[0], i)
        s = str( dobj.getValue( headers[0], i ) )
        for header in headers[1:]:
            s += "%10.3f" % (dobj.getValue( header, i ))
        print(s)

    
    print("\nTesting getColValues()")
    a = dobj.getColVals(headers)
    print(a)

    print("\nTesting data_range()")
    print(analysis.data_range(dobj, headers))

    print("\nTesting mean()")
    print(analysis.mean(dobj, headers))

    print("\nTesting stdev()")
    print(analysis.stdev(dobj, headers))

    print("\nTesting normalize_columns_seperately()")
    print(analysis.normalize_columns_seperately(dobj, headers))

    print("\nTesting normalize_columns_together()")
    print(analysis.normalize_columns_together(dobj, headers))


if __name__ == "__main__":
    main(sys.argv)




