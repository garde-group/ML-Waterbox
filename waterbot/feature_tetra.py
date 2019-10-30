'''
This is just a simple first attempt at some feature extraction. If this finds some success I can do more to improve it, I kinda want to try
GA hyperparameter optimization. Note for future attempts (group meeting):
-CNN (1D, 2D, 3D)
-Dense
-DeepHyperNEAT?????

Different amount of coordinates/cutoff?

Version 1.0
10/22/2019
Owen Lockwood
'''


import numpy as np
import keras
from keras import models
from keras import layers
from keras import optimizers
from keras import backend as K
import matplotlib.pyplot as plt


# Hardcoded defaults
NUM_COORD = 15
SIZE = 414200
IN_FILE = "tetra_coord.dat"

all_data = np.zeros(shape=(SIZE, NUM_COORD))
all_labels = np.zeros(shape=(SIZE))
count = 0

with open(IN_FILE) as f:
	for line in f:
		if (count >= SIZE):
			break
		l = line.split('    ')
		l = l[1:]
		l[15] = l[15].strip()		
		for i in range(len(l)):
			l[i] = float(l[i])
		all_data[count] = l[:NUM_COORD]
		all_labels[count] = l[NUM_COORD]
		count += 1

#print(all_data[:3])
#print(all_labels[:3])

'''
Centering the data, just one approach to try
'''
for i in range(SIZE):
	x = all_data[i][0]
	y = all_data[i][1]
	z = all_data[i][2]
	j = 3
	while (j < NUM_COORD):
		all_data[i][j] -= x
		all_data[i][j+1] -= y
		all_data[i][j+2] -= z
		j += 3
	all_data[i][0] = all_data[i][1] = all_data[i][2] = 0

#print(all_data[:3])
#print(all_labels[:3])

# To make each array into 2D like Sarupria paper
td_data = np.zeros(shape=(SIZE, 4, 3))
for i in range(SIZE):
	j = 3
	while (j < NUM_COORD):
		td_data[i][int(j/3)-1][0] = all_data[i][j]
		td_data[i][int(j/3)-1][1] = all_data[i][j+1]
		td_data[i][int(j/3)-1][2] = all_data[i][j+2]
		j += 3

print(td_data[0])
partial_train = td_data[:int(4*SIZE/5)]
partial_label = all_labels[:int(4*SIZE/5)]
val_data = td_data[int(4*SIZE/5):int(9*SIZE//10)]
val_label = all_labels[int(4*SIZE/5):int(9*SIZE//10)]
test_data = td_data[int(9*SIZE//10):]
test_label = all_labels[int(9*SIZE//10):]
#test_data = td_data[int(4*SIZE/5):]
#test_label = all_labels[int(4*SIZE/5):]
n = 4

cbs = [
    keras.callbacks.ModelCheckpoint("tetramodel.h5", monitor='val_mean_absolute_error', verbose=0, save_best_only=True)
]
np.save("test_data", test_data)
np.save("test_label", test_label)

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(4,3,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.MaxPooling1D(pool_size=4))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(1))
for layer in model.layers:
    print(layer.output_shape)
adam = optimizers.Adam(lr=0.001)
model.compile(optimizer=adam, loss='mse', metrics=['mae'])

history = model.fit(partial_train, partial_label, shuffle=True, epochs=30, \
batch_size=64, callbacks=cbs, validation_data=(val_data,val_label))

results = model.evaluate(test_data, test_label)
print(results[1])

average_mae_history = history.history['val_mean_absolute_error']

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
a = plt.figure(1)
plt.plot(range(1, len(average_mae_history) + 1), average_mae_history, 'blue', label='Average MAE')
plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history, 'olive', label='Smooth')
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
a.show()

plt.show()
