'''
This is a first attempt at using conv layers, instead of dense layers, to analyze water cavity size. I'm a little rusty and I have never worked with conv nets that much
before, so this will likely need some work.
I thought about 3d but it doesn't really make sense in my head yet. I'm going to try 1D with the 3 channels as x,y,z (sort of like RGB for 2d image analysis)


Version 1.0
Last Updated: 7/11/2019
Author(s): Owen Lockwood

7/12/19: It compiles and runs properly which is good, but preliminary testing indicates that it runs real bad. But maybe it doesn't I don't remember all the 
other results for box which was bad. Obviously model is not obtimised and probably is very bad but I want to check other's to compare it to (i.e. dense), then I can
try different conv approaches, like multichannel 1D -> 2D or a 3D approach? 

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

SIZE = 100000
BINARY = 83
RE = 84
NUMCOORD = 28
# The depth needs some characteristic? Is 1 for point and 0 for not a good way?
# data = np.zeros(shape=(SIZE, NUMCOORD, NUMCOORD, NUMCOORD, 1))
data = np.zeros(shape=(SIZE, 28, 3))
# Categorical or normal number for label?
labels = np.zeros(shape=SIZE, dtype=np.float)
counter = 0
with open("coord.dat") as f:
    for line in f:
        l = line.split('   ')
        final = []
        l = l[1:]
        i = 0
        while (i < BINARY):
            #print(i)
            data[counter][int((i+3)/3-1)][0] = l[i]
            data[counter][int((i+3)/3-1)][1] = l[i+1]
            data[counter][int((i+3)/3-1)][2] = l[i+2]
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
model = models.Sequential()
model.add(layers.Conv1D(100, 3, activation='relu', input_shape=(28, 3)))
model.add(layers.Conv1D(100, 3, activation='relu'))
model.add(layers.AveragePooling1D(3))
model.add(layers.Conv1D(160, 3, activation='relu'))
model.add(layers.Conv1D(160, 3, activation='relu'))
model.add(layers.GlobalAveragePooling1D())
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
