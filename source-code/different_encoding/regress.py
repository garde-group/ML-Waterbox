# 0 is for Owen
# This has a variety of different encodings imbedded in this code, hence why there are so many commented out sections
import keras 
from keras import models
from keras import layers 
from keras.models import load_model
from keras.utils import to_categorical
import numpy as np 
import matplotlib.pyplot as plt
import math

def vectorize_sequences(sequences, dimension=4000):
	results = np.zeros((len(sequences), dimension))
	for i in range(len(sequences)):
		for j in range(len(sequences[i])):
			#if int(sequences[i][j]) == 0:
			#	continue
			results[i][int(sequences[i][j])] = 1
	return results

def every_day_im_shuffling(a, b):
	rng_state = np.random.get_state()
	np.random.shuffle(a)
	np.random.set_state(rng_state)
	np.random.shuffle(b)

COORD = 84
SIZE = 150248
BINARY = 84
R = 85

data = np.zeros(shape=(SIZE,COORD))
labels = np.zeros(shape=SIZE, dtype=np.int64)
regression = np.zeros(shape=SIZE)
counter = 0
zero = 0
with open("test.dat") as f:
	for line in f:	
		if counter >= SIZE:
			break
		l = line.split('   ')
		final = []
		l = l[1:]
		for i in range(len(l)):
			final.append(float(l[i]))		
		#print(final[BINARY])
		if final[BINARY] == 1 and counter < SIZE:
			labels[counter]= final[BINARY]
			data[counter] = final[:BINARY]
			regression[counter] = final[R]
			counter += 1
		elif final[BINARY] == 0 and counter < SIZE and zero < (SIZE/2):
			labels[counter] = final[BINARY]
			data[counter] = final[:BINARY]
			regression[counter] = final[R]
			counter += 1
			zero += 1
		#print(data[counter])

print(data[:3])
print(regression[:3])
data1 = np.zeros(shape=(SIZE,6))
# This finds the nearest of the given coordinates to limit and fix the size
for i in range(len(data)):
	x = data[i][0]
	y = data[i][1]
	z = data[i][2]
	j = 3
	minl = 4
	minj = 4
	while (j < len(data[i])):
		dx = abs(data[i][j] - x)
		dy = abs(data[i][j+1] - y)
		dz = abs(data[i][j+2] - z)
		length = math.sqrt(dx**2 + dy**2 +dz**2)
		if (length < minl):
			minl = length
			minj = j
		j += 3
	data1[i][3] = data[i][minj] - x
	data1[i][4] = data[i][minj+1] - y
	data1[i][5] = data[i][minj+2] - z
	data1[i][0] = data1[i][1] = data1[i][2] = 0
	j = 6
	while (j < len(data[i])):
		data[i][j] = 0
		j += 1

'''
This shifts the points to the center
for i in range(len(data)):
	x = data[i][0]
	y = data[i][1]
	z = data[i][2]
	j = 3
	while (j < len(data[i])):
		if data[i][j] == 0:
			j += 3
			continue
		data[i][j] -= x
		data[i][j+1] -= y
		data[i][j+2] -= z
		j += 3
	data[i][0] = data[i][1] = data[i][2] = 0



for j in range(len(data)):
	for k in range(len(data[j])):
		data[j][k] *= 1000

data = vectorize_sequences(data)
'''
print(data[:3])
print(regression[:3])
every_day_im_shuffling(data1, regression) 

partial_train = data1[:int(SIZE/2)]
partial_label = regression[:int(SIZE/2)]
val_data = data1[int(SIZE/2):int(3*SIZE//4)]
val_label = regression[int(SIZE/2):int(3*SIZE//4)]
test_data = data1[int(3*SIZE//4):]
test_label = regression[int(3*SIZE//4):]

#print(labels[:100])

model = models.Sequential()
# This input shape needs to be changed to match whatever type of encoding you are doing, data1 has 6 indices, but the categorical has 4050
model.add(layers.Dense(6, activation='relu', input_shape=(6,)))
model.add(layers.Dense(3, activation='relu'))
model.add(layers.Dense(1))

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

history = model.fit(partial_train, partial_label, epochs=1000, batch_size=128, validation_data=(val_data, val_label))

#model.save('bench.h5')

results = model.evaluate(test_data, test_label)
print(results[1])
pred = model.predict(test_data)
# Seeing where the model is going wrong
#for i in range(len(pred)):
#	if pred[i] < 0.5 and test_label[i] == 1:
#		print("False Negative:", regression[i])


average_mae_history = history.history['val_mean_absolute_error']
# Standard plotting idea
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
plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

a.show()
b.show()


plt.show()


