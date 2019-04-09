# 0 is for Owen
import keras 
from keras import models
from keras import layers 
from keras.models import load_model
from keras.utils import to_categorical
import numpy as np 
import matplotlib.pyplot as plt
import math

def every_day_im_shuffling(a, b):
	rng_state = np.random.get_state()
	np.random.shuffle(a)
	np.random.set_state(rng_state)
	np.random.shuffle(b)

COORD = 84
SIZE = 500000
BINARY = 84
R = 85

data = np.zeros(shape=(SIZE,COORD))
regression = np.zeros(shape=SIZE)
counter = 0
with open("8box.dat") as f:
	for line in f:	
		l = line.split('   ')
		final = []
		l = l[1:]
		for i in range(len(l)):
			final.append(float(l[i]))		
		data[counter] = final[:COORD]
		regression[counter] = final[R]
		counter += 1

print(data[:3])
print(regression[:3])
for i in range(len(data)):
	x = data[i][0]
	y = data[i][1]
	z = data[i][2]
	j = 3
	while (j < len(data[i])):
		if data[i][j] == 0:
			# Instead of 0s make them all on the box edge
			data[i][j] = 0.25
			data[i][j+1] = 0.25
			data[i][j+2] = 0.25
			j += 3
			continue
		data[i][j] -= x
		data[i][j+1] -= y
		data[i][j+2] -= z
		j += 3
	data[i][0] = data[i][1] = data[i][2] = 0

print(data[:3])
print(regression[:3])
every_day_im_shuffling(data, regression) 

partial_train = data[:int(SIZE/2)]
partial_label = regression[:int(SIZE/2)]
val_data = data[int(SIZE/2):int(3*SIZE//4)]
val_label = regression[int(SIZE/2):int(3*SIZE//4)]
test_data = data[int(3*SIZE//4):]
test_label = regression[int(3*SIZE//4):]


model = models.Sequential()
model.add(layers.Dense(84, activation='relu', input_shape=(84,)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1))

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

history = model.fit(partial_train, partial_label, shuffle=False, epochs=1000, batch_size=128, validation_data=(val_data, val_label))

#model.save('bench.h5')

results = model.evaluate(test_data, test_label)
print(results[1])
pred = model.predict(test_data)

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
plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

a.show()
b.show()


plt.show()



