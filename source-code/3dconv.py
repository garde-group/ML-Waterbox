'''
This is the first attempted implementation of another idea I had. Since the 1D conv was worth a try, but I doubt that practically or conceptually it will go 
anywhere, I am trying to implement a 3D version that makes (somewhat) more conceptual sense. Conv really makes sense for pictures or data that is borken down
into "pixels" and since normal coordinates can be placed into that, make each coordinate into a whole number and it can. A 3d image where each slot in the array
corresponds to a certain point in the smallest precision the coordinates are generated at.


Author: Owen Lockwood
Version 1.0
Last Modified: 7/28/19
'''

import keras
import numpy as np
import matplotlib.pyplot as plt
from keras import models
from keras import layers
from keras.utils import plot_model


def every_day_im_shuffling(a, b):
	rng_state = np.random.get_state()
	np.random.shuffle(a)
	np.random.set_state(rng_state)
	np.random.shuffle(b)

SIZE = 100000 # THIS IS TOO BIG TO LOAD INTO RAM MEMORY, I HAVE 20 GB/32 GB USABLE AT TIME OF RUNNING ON MY LAPTOP AND THAT IS NOT ENOUGH
# NEED TO MAKE A GENERATOR
BINARY = 83
RE = 84
NUMCOORD = 28
# The depth needs some characteristic? Is 1 for point and 0 for not a good way?
# data = np.zeros(shape=(SIZE, NUMCOORD, NUMCOORD, NUMCOORD, 1))
data = np.zeros(shape=(SIZE, 4000, 4000, 4000))
# Categorical or normal number for label?
labels = np.zeros(shape=SIZE, dtype=np.float)
counter = 0
with open("coord.dat") as f:
    for line in f:
        l = line.split('   ')
        final = []
        l = l[1:]
        i = 0
        if (counter <= SIZE):
            break
        while (i < BINARY):
            #print(i)
            data[counter][int(l[i]*1000)][int(l[i+1]*1000)][int(l[i+2]*1000)] = 1
            i += 3
        labels[counter] = l[RE]
        counter += 1

every_day_im_shuffling(data, labels) 
partial_train = data[:int(SIZE/2)]
partial_label = labels[:int(SIZE/2)]
val_data = data[int(SIZE/2):int(3*SIZE//4)]
val_label = labels[int(SIZE/2):int(3*SIZE//4)]
test_data = data[int(3*SIZE//4):]
test_label = labels[int(3*SIZE//4):]

# Max pooling vs average pooling?
# What to make kernal size???
model = models.Sequential()
model.add(layers.Conv3D(100, (100,100,100), activation='relu', input_shape=(4000, 4000, 4000, 1)))
model.add(layers.Conv3D(100, (100,100,100), activation='relu'))
model.add(layers.AveragePooling1D((200,200,200)))
model.add(layers.Conv3D(160, (100,100,100), activation='relu'))
model.add(layers.Conv3D(160, (100,100,100), activation='relu'))
model.add(layers.GlobalAveragePooling3D())
model.add(layers.Flatten())
model.add(layers.Dense(1))


class debug_callback(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        pass

c1 = debug_callback()
callbacklist = [
    c1, 
    keras.callbacks.TensorBoard(log_dir='temp', histogram_freq=1, batch_size=128, write_graph=True, write_grads=True, \
    write_images=True, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None, embeddings_data=None, update_freq='epoch')
]

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
history = model.fit(partial_train, partial_label, epochs=30, batch_size=128, validation_data=(val_data, val_label), callbacks=callbacklist)

results = model.evaluate(test_data, test_label)
print(results[1])
plt.rcParams.update({'font.size': 30})

average_mae_history = history.history['val_mean_absolute_error']

a = plt.figure(1)
plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')

def smooth_curve(points, factor=0.9):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points

smooth_mae_history = smooth_curve(average_mae_history[10:])
b = plt.figure(2)
plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history, 'b')
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

a.show()
b.show()


plt.show()