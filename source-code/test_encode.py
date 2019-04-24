# This was a program I made to test the different encoding strategies against random coordinates
import keras 
from keras import models
from keras import layers 
from keras.models import load_model
import numpy as np 
import matplotlib.pyplot as plt
import math
import random

def vectorize_sequences(sequences, dimension=4000):
	results = np.zeros((len(sequences), dimension))
	for i in range(len(sequences)):
		for j in range(len(sequences[i])):
			results[i][int(sequences[i][j])] = 1
	return results

def createmodel(insize):
    model = models.Sequential()
    model.add(layers.Dense(60, activation='relu', input_shape=(insize,)))
    model.add(layers.Dense(30, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    return model

onehot = dict()
onehot["trainacc"] = []
onehot["trainloss"] = []
onehot["valacc"] = []
onehot["valloss"] = []
normalize = dict()
normalize["trainacc"] = []
normalize["trainloss"] = []
normalize["valacc"] = []
normalize["valloss"] = []
centered = dict()
centered["trainacc"] = []
centered["trainloss"] = []
centered["valacc"] = []
centered["valloss"] = []

for i in range(20):
    # Number of "water molecules" to give it
    starting = np.random.rand(100000, int(3*(i+1)))
    # 100,000 total data
    starting *= 4
    # Now we must split it into the three types of encodings I am testing: categorical, normalized, and centered
    print(starting[:3])
    labels = np.zeros(shape=100000)
    test = 0
    for j in range(len(starting)):
        k = 0
        cave = True
        while k < len(starting[j]):
            dx = abs(2 - starting[j][k])
            dy = abs(2 - starting[j][k+1])
            dz = abs(2 - starting[j][k+2])
            length = math.sqrt(dx**2 + dy**2 + dz**2)
            if length < 1.97:
                cave = False
            k += 3
        if cave:
            test += 1
            labels[j] = 1

    #print(test)
    categorical = normal = center = starting
    categorical *= 1000
    mean = normal.mean()
    normal -= mean 
    std = normal.std()
    normal /= std
    center -= 2
    
    hot = vectorize_sequences(categorical)
    # Create the models
    hotmodel = createmodel(4000)
    normalmodel = createmodel(int(3*(i+1)))
    centermodel = createmodel(int(3*(i+1)))
    
    # Split validation and training, test doesn't really matter that much for this example
    train_hot = hot[:75000]
    val_hot = hot[75000:]
    train_normal = normal[:75000]
    val_normal = normal[75000:]
    train_center = center[:75000]
    val_center = center[75000:]
    train_label = labels[:75000]
    val_label = labels[75000:]

    # Traing the models, record the output, and plot it to be saved and viewed by the user
    hot_history = hotmodel.fit(train_hot, train_label, shuffle=False, epochs=100, batch_size=256, validation_data=(val_hot, val_label))
    normal_history = normalmodel.fit(train_normal, train_label, shuffle=False, epochs=100, batch_size=256, validation_data=(val_normal, val_label))
    center_history = centermodel.fit(train_center, train_label, shuffle=False, epochs=100, batch_size=256, validation_data=(val_center, val_label))
    keras.backend.clear_session()
    onehot["trainacc"] = hot_history.history['acc']
    onehot["trainloss"] = hot_history.history['loss']
    onehot["valacc"] = hot_history.history['val_acc']
    onehot["valloss"] = hot_history.history['val_loss']

    normalize["trainacc"] = normal_history.history['acc']
    normalize["trainloss"] = normal_history.history['loss']
    normalize["valacc"] = normal_history.history['val_acc']
    normalize["valloss"] = normal_history.history['val_loss']

    centered["trainacc"] = center_history.history['acc']
    centered["trainloss"] = center_history.history['loss']
    centered["valacc"] = center_history.history['val_acc']
    centered["valloss"] = center_history.history['val_loss']

    print(3*(i+1))
    size = np.arange(1,101)
    a = plt.figure(1)
    plt.plot(size, onehot["trainacc"], label='Categorical')
    plt.plot(size, normalize["trainacc"], label='Normalized')
    plt.plot(size, centered["trainacc"], label='Centered')
    plt.title('Training Accuracies')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    b = plt.figure(2)
    plt.plot(size, onehot["valacc"], label='Categorical')
    plt.plot(size, normalize["valacc"], label='Normalized')
    plt.plot(size, centered["valacc"], label='Centered')
    plt.title('Validation Accuracies')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    c = plt.figure(3)
    plt.plot(size, onehot["trainloss"], label='Categorical')
    plt.plot(size, normalize["trainloss"], label='Normalized')
    plt.plot(size, centered["trainloss"], label='Centered')
    plt.title('Training Loses')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Loss')
    plt.legend()

    d = plt.figure(4)
    plt.plot(size, onehot["valloss"], label='Categorical')
    plt.plot(size, normalize["valloss"], label='Normalized')
    plt.plot(size, centered["valloss"], label='Centered')
    plt.title('Validation Loses')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Loss')
    plt.legend()


    a.show()
    b.show()
    c.show()
    d.show()

    plt.show()
