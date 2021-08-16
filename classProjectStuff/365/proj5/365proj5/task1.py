from __future__ import print_function
import os
import cv2
import numpy as np
import scipy
import matplotlib
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


choice = int(input("Enter 1 to retrain the whole model and output it, Enter 0 to just identify images using a prebuilt model!\n"))


if(choice == 1):
    np.random.seed(42)

    batchSize = 128
    numClasses = 10
    epochs = 10

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
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(numClasses, activation='softmax'))

    #compiling the network
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    #training and outputting a score from the test set
    model.fit(xTrain, yTrain, batch_size=batchSize, epochs=epochs, verbose=1, validation_data=(xTest, yTest))
    score = model.evaluate(xTest, yTest, verbose=1)

    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    #saving model to JSON file
    modelJSON = model.to_json()
    with open("model.json", 'w') as out:
        out.write(modelJSON)

    #saving weights 
    model.save_weights("model.h5")
    print("Successfully Saved Model!")
else:
    #loading back in the model
    jsonIn = open("model.json", "r")
    loadedModel = jsonIn.read()
    jsonIn.close()
    model = model_from_json(loadedModel)

    #loading weights in
    model.load_weights("model.h5")

    print("Successfully loaded model and weights!")

    directory = os.fsencode("numpics")

    for filee in os.listdir(directory):
        filename = os.fsdecode(filee)
        if filename.endswith(".jpg"):
            filename = "./numpics/"+filename
            img = cv2.imread(filename)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.resize(img, (28,28))

            cv2.imshow("lol", img)
            cv2.waitKey(0)

            img = img.reshape( (1,) + img.shape + (1,) )

            classList = model.predict(img).tolist()[0]

            idx = classList.index(max(classList))
            print(classList)
            print(f"The max index was {idx} which classifies the image as the digit {idx}")


    # (xTrain, yTrain), (xTest, yTest) = mnist.load_data()

    # for i in range(25):
    #     img = xTest[i]

    #     cv2.imshow("Window", img)
    #     cv2.waitKey(0)
    #     img = img.reshape( (1,) + img.shape + (1,) )

    #     classList = model.predict(img).tolist()[0]

    #     idx = classList.index(max(classList))
    #     print(f"The max index was {idx} which classifies the image as the digit {idx}")
    

        





