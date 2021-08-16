from __future__ import print_function
import os
import cv2
import csv
import numpy as np
import scipy
import matplotlib
import matplotlib.pyplot as plt
import keras
from keras.datasets import mnist
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

#comment this stuff out if not using a GPU
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)
#End comment here

#loading back in the model
jsonIn = open("model.json", "r")
loadedModel = jsonIn.read()
jsonIn.close()
model = model_from_json(loadedModel)

#loading weights in
model.load_weights("model.h5")

print("Successfully loaded model and weights! \n\n")


#reading in the greek letter images and creating the csvs
dirname = "greekletterswithnew"
directory = os.fsencode(dirname)
output1 = open("output1.csv", "w")
output2 = open("output2.csv", "w")

for filee in os.listdir(directory):
    filename = os.fsdecode(filee)
    if filename.endswith(".png"):
        basefilename = filename
        filename = "./"+dirname+"/"+filename
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (28,28))

        header = basefilename
        output1.write(header+",")
        count = 0
        for r in range(28):
            for c in range(28):
                output1.write(str(img[r,c]) +",")

        output1.write("\n")

        output2.write(header+",")
        if basefilename.startswith("alpha"):
            output2.write(str(0))
        elif basefilename.startswith("beta"):
            output2.write(str(1))
        elif basefilename.startswith("gamma"):
            output2.write(str(2))
        else:
            output2.write(str(-1))
        
        output2.write("\n")

output1.close()
output2.close()

#new model stuff
(xTrain, yTrain), (xTest, yTest) = mnist.load_data()
firstin = xTrain[0]

firstin = firstin.reshape( (1,) + firstin.shape + (1,) )


layerouts = [layer.output for layer in model.layers[:-2]]
newmodel = keras.Model( inputs=model.input, outputs=layerouts )

firstpred = newmodel.predict(firstin)[len(layerouts)-1][0]
print(f"Output of first input prediction with truncated network, should be 128: length {len(firstpred)} \n")
#print(firstpred)

#Applying network to the greek letters
featureVectors = []

csvin = open("output1.csv", "r")
lines = csvin.readlines()

for line in lines:
    vals = str.split(line, ",")[1:-1] #to -1 because I have an extra comma that I was too lazy to get rid of :)
    
    imgvals = []
    currow = []
    img = np.ndarray((28,28))

    row = 0
    col = 0
    for idx in range(784):
        img[row, col] = int(vals[idx])
        col += 1
        #currow.append(int(vals[idx]))
        if(col%28 == 0  ):
            col = 0
            row += 1
            #imgvals.append(currow)
            #currow = []

    #img = np.matrix(imgvals)
    img = img.reshape( (1,) + img.shape + (1,) )

    predlist = newmodel.predict(img)[len(layerouts)-1][0]
    featureVectors.append(predlist)

print(f"This list contains all the feature vectors from the CNN it should be length 27: length: {len(featureVectors)} \n" )

#Calculating SSD stuff for the first 3 letters of each category
aIdx = 28 #0 #27,28
bIdx = 30 #9 #29,30
gIdx = 32 #18 #31,32
alpha = featureVectors[aIdx]
beta = featureVectors[bIdx]
gamma = featureVectors[gIdx]
aSSDs, bSSDs, gSSDs = [],[],[]

for vector in featureVectors:
    aSSD = np.sum(np.square(alpha - vector))
    bSSD = np.sum(np.square(beta - vector))
    gSSD = np.sum(np.square(gamma - vector))
    aSSDs.append(aSSD)
    bSSDs.append(bSSD)
    gSSDs.append(gSSD)

aMinIdx = aSSDs.index(min(aSSDs))
bMinIdx = bSSDs.index(min(bSSDs))
gMinIdx = gSSDs.index(min(gSSDs))

del aSSDs[aMinIdx]
aMatch = aSSDs.index(min(aSSDs))
del bSSDs[bMinIdx]
bMatch = bSSDs.index(min(bSSDs))
del gSSDs[gMinIdx]
gMatch = gSSDs.index(min(gSSDs))

matchIdxs = [aMatch, bMatch, gMatch]

classes = []
for minIdx in matchIdxs:
    if(minIdx < 9):
        classes.append("alpha")
    elif(minIdx < 18):
        classes.append("beta")
    elif(minIdx < 27):
        classes.append("gamma")
    else:
        classes.append("unmatched to any known class")

print(f"SSDs to the first alpha char, 0.0 should be at index {aIdx}\n {aSSDs}\n")
print(f"Min value found at index: {aMinIdx}\n")

print(f"SSDs to the first beta char, 0.0 should be at index {bIdx}\n {bSSDs} \n")
print(f"Min value found at index: {bMinIdx}\n")

print(f"SSDs to the first gamma char, 0.0 should be at index {gIdx}\n {gSSDs} \n")
print(f"Min value found at index: {gMinIdx}\n")

print(f"If we were to match these to the nearest besides themselves they would identify as the following (in order)\n{classes}\n")




