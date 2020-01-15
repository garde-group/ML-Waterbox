import numpy as np
import keras
from keras import models
from keras import layers
from keras import optimizers
from keras import backend as K
import matplotlib.pyplot as plt
import random
import math


# Hardcoded defaults
NUM_COORD = 33
SIZE = 500000

td_data = np.zeros(shape=(SIZE, 10, 3))
all_labels = np.zeros(shape=(SIZE))
for i in range(SIZE):
    max_len = 10
    for j in range(10):
	'''
	td_data[i][j][0] = random.uniform(-0.6,0.6)
	td_data[i][j][1] = random.uniform(-0.6,0.6)
	td_data[i][j][2] = random.uniform(-0.6,0.6)
	d = math.sqrt(td_data[i][j][0]**2+td_data[i][j][1]**2+td_data[i][j][2]**2)
	while d > 0.6:
		td_data[i][j][0] = random.uniform(-0.6,0.6)
		td_data[i][j][1] = random.uniform(-0.6,0.6)
		td_data[i][j][2] = random.uniform(-0.6,0.6)
		d = math.sqrt(td_data[i][j][0]**2+td_data[i][j][1]**2+td_data[i][j][2]**2)
	'''
	d = random.uniform(0,0.6) * 2 + random.random()*0.2
	td_data[i][j][0] = x = math.sqrt(random.uniform(0,d**2)) * (-1 if random.random() < 0.5 else 1)
	td_data[i][j][1] = y = math.sqrt(random.uniform(0, d**2-x**2)) * (-1 if random.random() < 0.5 else 1)
	td_data[i][j][2] = z = math.sqrt(d**2-x**2-y**2) * (-1 if random.random() < 0.5 else 1)
	#if abs((d - math.sqrt(x**2+y**2+z**2))) > 0.001:
	#	print(d, x, y, z, math.sqrt(x**2+y**2+z**2))
	#	m = input()
	#max_len = min(max_len, d)        
	max_len = min(max_len, math.sqrt(td_data[i][j][0]**2 + td_data[i][j][1]**2 + td_data[i][j][2]**2))
    all_labels[i] = max_len

plt.hist(all_labels)
plt.show()
print(td_data[0], all_labels[0])
partial_train = td_data[:int(4*SIZE/5)]
partial_label = all_labels[:int(4*SIZE/5)]
val_data = td_data[int(4*SIZE/5):int(9*SIZE//10)]
val_label = all_labels[int(4*SIZE/5):int(9*SIZE//10)]
test_data = td_data[int(9*SIZE//10):]
test_label = all_labels[int(9*SIZE//10):]

n = 4
cbs = [
    keras.callbacks.ModelCheckpoint("cave_gen_distribution.h5", monitor='val_mean_absolute_error', verbose=0, save_best_only=True)
]

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10,3,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.MaxPooling1D(pool_size=10))
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


