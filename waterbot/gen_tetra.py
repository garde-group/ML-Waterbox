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
SIZE = 500000

td_data = np.zeros(shape=(SIZE, 4, 3))
all_labels = np.zeros(shape=(SIZE))
for i in range(SIZE):
    tet = random.uniform(-0.3,1.0)
    while True:
	    for j in range(4):
		td_data[i][j][0] = x = random.uniform(-0.5,0.5) 
		td_data[i][j][1] = y = random.uniform(-0.5,0.5)
		td_data[i][j][2] = z = random.uniform(-0.5,0.5)
		'''	
		if x * y > 1:
			x = 1-x
			y = 1-y
		if y * z > 1:
			y = 1 - y
			z = 1 - z
		elif x*y*z > 1:
			temp = x	
			x = x*y*z-1
			y = 1 - z - temp
		a = 1 - x - y - z	
		#final = map(lambda c, v, b, g: c+v+b+g, v0,v1,v2,v3)    	
		'''
		if abs(x + y) > 0.5:
			x = 0.5 - x
			y = 0.5 - y
		if abs(x + y + z) > 0.5:
			if abs(y + z) > 0.5:
				y = 0.5 - z
				z = 0.5 - x - y
			else:
				x = 0.5 - y - z
				z = x + y + z - 0.5
		final = [x,y,z]	
		td_data[i][j][0] = final[0]
		td_data[i][j][1] = final[1]
		td_data[i][j][2] = final[2]
		#print(final)
		#j = input()
	    m = 0
	    n = 1
	    sigma = 0
	    while m < 3:
		while n < 4:
			a = math.sqrt(td_data[i][m][0]**2 + td_data[i][m][1]**2 + td_data[i][m][2]**2)
			b = math.sqrt(td_data[i][n][0]**2 + td_data[i][n][1]**2 + td_data[i][n][2]**2)
			dx = td_data[i][m][0] - td_data[i][n][0]
			dy = td_data[i][m][1] - td_data[i][n][1]
			dz = td_data[i][m][2] - td_data[i][n][2]
			c = math.sqrt(dx**2 + dy**2 + dz**2)
			angle = (c**2 - a**2 - b**2) / (-2 * b * a)
			angle = (angle + 1./3.)**2
			sigma += angle
			n += 1
		m += 1
	    t = 1 - 3./8. * sigma
	    all_labels[i] = t
 	    if abs(t-tet) < 0.3:
		break
print(all_labels[:5])
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
    keras.callbacks.ModelCheckpoint("tetra_gen1.h5", monitor='val_mean_absolute_error', verbose=0, save_best_only=True)
]

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(4,3,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(256, activation='relu'))
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


