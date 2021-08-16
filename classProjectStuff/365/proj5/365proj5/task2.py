from __future__ import print_function
import os
import cv2
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

print("Successfully loaded model and weights!")


#first layer images
layer = model.get_layer(index=0)

filters = np.asarray(layer.get_weights())[0]

#normalizing
maxval = filters.max()
minval = filters.min()
absmax = max(abs(minval),abs(maxval))

filters = (filters / absmax)*255
figure1, subplots = plt.subplots(nrows=8, ncols=4)

idx = 0
for row in subplots:
    for col in row:
        curfilt = filters[:,:,0,idx]
        idx += 1
        print(curfilt)

        finalImage = np.zeros((curfilt.shape[0],curfilt.shape[1],3), np.uint8)
        for r in range(finalImage.shape[0]):
            for c in range(finalImage.shape[1]):
                if(curfilt[r,c] < 0):
                    finalImage[r,c,0] = curfilt[r,c]
                else:
                    finalImage[r,c,1] = curfilt[r,c]

        col.imshow(finalImage)


#first image with the 32 different filters
(xTrain, yTrain), (xTest, yTest) = mnist.load_data()
firstImg = xTrain[0]

figure2, subplots = plt.subplots(nrows=8, ncols=4)
idx = 0
for row in subplots:
    for col in row:
        curfilt = filters[:,:,0,idx]
        idx += 1

        finalImage = cv2.filter2D(firstImg, -1, curfilt)

        col.imshow(finalImage)

#image after first layer
firstImg = xTrain[0]


firstLayerModel = keras.Model( inputs=model.input, outputs=model.get_layer(index=0).output )

img = firstImg.reshape( (1,) + firstImg.shape + (1,) )

outputImg = firstLayerModel.predict(img)

figure3, subplots = plt.subplots(nrows=8, ncols=4)
idx = 0
for row in subplots:
    for col in row:
        curimg = outputImg[0,:,:,idx]
        idx += 1
        col.imshow(curimg)



#Image after first two layers

firstImg = xTrain[0]

layerouts = [layer.output for layer in model.layers[:2]]
firstTwoLayerModel = keras.Model( inputs=model.input, outputs=layerouts )


img = firstImg.reshape( (1,) + firstImg.shape + (1,) )

outputImg = firstTwoLayerModel.predict(img)

outputImg = outputImg[1]

figure4, subplots = plt.subplots(nrows=8, ncols=4)
idx = 0
for row in subplots:
    for col in row:
        curimg = outputImg[0,:,:,idx]
        idx += 1
        col.imshow(curimg)


#Image after first 3 layers
firstImg = xTrain[3]

layerouts = [layer.output for layer in model.layers[:3]]
firstTwoLayerModel = keras.Model( inputs=model.input, outputs=layerouts )


img = firstImg.reshape( (1,) + firstImg.shape + (1,) )

outputImg = firstTwoLayerModel.predict(img)

outputImg = outputImg[2]

figure4, subplots = plt.subplots(nrows=8, ncols=4)
idx = 0
for row in subplots:
    for col in row:
        curimg = outputImg[0,:,:,idx]
        idx += 1
        col.imshow(curimg)



plt.show()


