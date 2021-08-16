from __future__ import print_function
import os
import cv2
import numpy as np
import scipy
import matplotlib
import keras
import time
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


np.random.seed(42)

def testModel(batchSize=128, epochs=10, denseCount=128, dropoutval2=.5):

    numClasses = 10

    # input image dimensions
    imgRows, imgCols = 28, 28

    #loading in dataset
    (xTrain, yTrain), (xTest, yTest) = mnist.load_data()

    # 28x28 1 grayscale channel
    xTrain = xTrain.reshape(xTrain.shape[0], imgRows, imgCols, 1)
    xTest = xTest.reshape(xTest.shape[0], imgRows, imgCols, 1)

    xTrain = xTrain.astype('float32')
    xTest = xTest.astype('float32')

    #Normalizing so each pizel goes from 0 to 1 instead of 0 to 255
    xTrain /= 255
    xTest /= 255

    #one-hot encoding
    yTrain = keras.utils.to_categorical(yTrain, numClasses)
    yTest = keras.utils.to_categorical(yTest, numClasses)

    #Making the network
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=(28,28,1)))
    model.add(Conv2D(32, (3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(.25))
    model.add(Flatten())
    model.add(Dense(denseCount, activation='relu'))
    model.add(Dropout(dropoutval2))
    model.add(Dense(numClasses, activation='softmax'))


    #compiling the network
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    curtime = int(round(time.time() * 1000))

    #training and outputting a score from the test set
    model.fit(xTrain, yTrain, batch_size=batchSize, epochs=epochs, verbose=0, validation_data=(xTest, yTest))

    trainingtime = int(round(time.time() * 1000)) - curtime

    score = model.evaluate(xTest, yTest, verbose=0)

    print(f'---Test Parameters---\nBatch Size: {batchSize}\nEpochs: {epochs}\nDense Hidden Nodes: {denseCount}')
    print('---Test Results---')
    print(f'Training Time (ms): {trainingtime}')
    print('Test loss: ', score[0])
    print('Test accuracy: ', score[1], "\n")

    return score[1], trainingtime


def main():
    batchSizeList = [64,128,256]
    epochsList = [8,10,12]
    denseNodesList = [64,128,256]
    droupoutvalList = [.3, .7]

    file = open("modeltestingoutput.txt", "w")


    print("\n-------CHECKING BATCH SIZE CHANGES--------\n")
    maxscore = -1
    batchidx = 0
    curidx = 0
    for val in batchSizeList:
        curscore, traintime = testModel(batchSize=val)
        file.write(f"Batch Size:{batchSizeList[curidx]} Epochs:{10} Dense Count:{128} 2nd Dropout %:{.5}\n")
        file.write(f"Accuracy: {curscore}\n")
        file.write(f"Train Time: {traintime}\n\n")
        curidx += 1
        if(curscore > maxscore):
            maxscore = curscore
            batchidx = batchSizeList.index(val)
    
    print("\n-------CHECKING EPOCH CHANGES--------\n")
    maxscore = -1
    curidx = 0
    epochidx = 0
    for val in epochsList:
        curscore, traintime = testModel(epochs=val)
        file.write(f"Batch Size:{128} Epochs:{epochsList[curidx]} Dense Count:{128} 2nd Dropout %:{.5}\n")
        file.write(f"Accuracy: {curscore}\n")
        file.write(f"Train Time: {traintime}\n\n")
        curidx += 1

    print("\n-------CHECKING DENSE NODE CHANGES--------\n")
    maxscore = -1
    curidx = 0
    denseidx = 0
    for val in denseNodesList:
        curscore, traintime = testModel(denseCount=val)
        file.write(f"Batch Size:{128} Epochs:{10} Dense Count:{denseNodesList[curidx]} 2nd Dropout %:{.5}\n")
        file.write(f"Accuracy: {curscore}\n")
        file.write(f"Train Time: {traintime}\n\n")
        curidx += 1

    print("\n-------CHECKING DROPOUT CHANGES--------\n")
    maxscore = -1
    dropoutidx = 0
    curidx = 0
    for val in droupoutvalList:
        curscore, traintime = testModel(dropoutval2=val)
        file.write(f"Batch Size:{128} Epochs:{10} Dense Count:{128} 2nd Dropout %:{droupoutvalList[curidx]}\n")
        file.write(f"Accuracy: {curscore}\n")
        file.write(f"Train Time: {traintime}\n\n")
        curidx += 1    

    print("\n--------CHECKING VARYING DENSE/BATCH TOGETHER-------")
    maxscore = -1
    denseidx = 0
    batchidx = 0
    curbatch = 0
    curdense = 0
    for i in range(9):
        curscore, traintime = testModel(batchSize=batchSizeList[curbatch], denseCount=denseNodesList[curdense])
        file.write(f"Batch Size:{batchSizeList[curbatch]} Epochs:{10} Dense Count:{denseNodesList[curdense]} 2nd Dropout %:{.5}\n")
        file.write(f"Accuracy: {curscore}\n")
        file.write(f"Train Time: {traintime}\n\n")
        curdense += 1
        if(curdense % 3 == 0):
            curdense = 0
            curbatch += 1
    
    print("\n-----The following combination of batch/dense values had the highest accuracy-----")
    print(f"Batch Size: {batchSizeList[batchidx]}\nEpochs: {10}\nDense Count: {denseNodesList[denseidx]}\n2nd Dropout %: {.5}\n")
    

    file.close()


if __name__ == "__main__":
    main()
