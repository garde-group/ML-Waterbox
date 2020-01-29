'''
Version Notes
1.0: Creation



Version 1.0
1/28/2020
Owen Lockwood
'''


import numpy as np
import keras
import math
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
cav_labels = np.zeros(shape=(SIZE))
td_data = np.zeros(shape=(SIZE, 4, 3))
for i in range(SIZE):
	j = 3
	while (j < NUM_COORD):
		td_data[i][int(j/3)-1][0] = all_data[i][j]
		td_data[i][int(j/3)-1][1] = all_data[i][j+1]
		td_data[i][int(j/3)-1][2] = all_data[i][j+2]
		j += 3
	dist = 5
	for k in range(4):
		dx = abs(td_data[i][k][0])
		if dx > 2.5:
			dx -= 5
		dy = abs(td_data[i][k][1])
		if dy > 2.5:
			dy -= 5
		dz = abs(td_data[i][k][2])
		if dz > 2.5:
			dz -= 5
		temp = math.sqrt(dx**2 + dy**2 + dz**2)
		if temp < dist:
			dist = temp
	if dist > 1:
		print(dist, td_data[i])
	cav_labels[i] = dist

print(td_data[0])
partial_train = td_data[:int(4*SIZE/5)]
partial_label = all_labels[:int(4*SIZE/5)]
val_data = td_data[int(4*SIZE/5):int(9*SIZE//10)]
val_label = all_labels[int(4*SIZE/5):int(9*SIZE//10)]
test_data = td_data[int(9*SIZE//10):]
test_label = all_labels[int(9*SIZE//10):]
partial_label_cav = cav_labels[:int(4*SIZE/5)]
val_label_cav = cav_labels[int(4*SIZE/5):int(9*SIZE//10)]
test_label_cav = cav_labels[int(9*SIZE//10):]
n = 4

cbs = [
    keras.callbacks.ModelCheckpoint("multi_head_cave.h5", monitor='val_cave_out_mean_absolute_error', verbose=0, save_best_only=True)
]
#np.save("test_data", test_data)
#np.save("test_label", test_label)

input_shape = (4,3)
inputs = layers.Input(input_shape)
x = layers.Dense(32, activation='relu', name='feature1')(inputs)
x = layers.Dense(64, activation='relu', name='feature2')(x)
x = layers.Dense(128, activation='relu', name='feature3')(x)
x = layers.Dense(256, activation='relu', name='feature4')(x)
x = layers.Dense(512, activation='relu', name='feature5')(x)
x = layers.Dense(1024, activation='relu', name='feature6')(x)
x = layers.MaxPooling1D(pool_size=4)(x)
x = layers.Flatten()(x)
x = layers.Dropout(0.3)(x)

tetra = layers.Dense(512, activation='relu', name='tetra1')(x)
tetra = layers.Dense(256, activation='relu', name='tetra2')(tetra)
#tetra = layers.Dropout(0.3)(tetra)
tetra = layers.Dense(1, name='tetra_out')(tetra)

cave = layers.Dense(512, activation='relu', name='cave1')(x)
cave = layers.Dense(256, activation='relu', name='cave2')(cave)
#cave = layers.Dropout(0.3)(cave)
cave = layers.Dense(1, name='cave_out')(cave)

adam = optimizers.Adam(lr=0.001)

model = models.Model(inputs=inputs, outputs=[cave, tetra])

model.compile(loss={'cave_out': 'mse', 'tetra_out': 'mse'}, metrics={'cave_out': 'mae', 'tetra_out': 'mae'}, optimizer=adam)

history = model.fit(partial_train, [partial_label_cav, partial_label], shuffle=True, epochs=50, \
batch_size=64, callbacks=cbs, validation_data=(val_data, [val_label_cav, val_label]))

results = model.evaluate(test_data, [test_label_cav, test_label])
print(results[1])

average_mae_history = history.history['val_mean_absolute_error']

a = plt.figure(1)
plt.plot(range(1, len(average_mae_history) + 1), average_mae_history, 'blue', label='Average MAE')
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')



a.show()

plt.show()

