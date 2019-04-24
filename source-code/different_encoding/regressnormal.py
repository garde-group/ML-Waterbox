# 0 is for Owen
# This version is based on the normalization of the coordinates
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

# Same input variables as always, size and locations of the information
COORD = 84
SIZE = 150248
BINARY = 84
R = 85

data = np.zeros(shape=(SIZE,COORD))
labels = np.zeros(shape=SIZE, dtype=np.int64)
regression = np.zeros(shape=SIZE)
counter = 0
zero = 0
# Reading in the file
# Note: The restrictions on size in this file and on all regression problems ought to be removed
# There is no need to have equal 1s and zeros if there it isn't a binary classification problem
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
# Because the default 0s don't matter when calculating std and mean (because they are padded values), this is one approach
# There exists default functions in numpy to do this that would also work
for i in range(len(data)):
    summ = 0
    numm = 0
    for j in range(len(data[i])):
        if data[i][j] == 0:
            continue
        summ += data[i][j]
        numm += 1
    mean = summ / numm
    std = 0
    summ = 0
    for j in range(len(data[i])):
        if data[i][j] == 0:
            continue
        std += (data[i][j] - mean)**2
        data[i][j] -= mean
    std = math.sqrt(std/numm)**2
    data[i] /= std

print(data[:3])
print(regression[:3])
# Shuffle then split
every_day_im_shuffling(data,regression)

partial_train = data[:int(SIZE/2)]
partial_label = regression[:int(SIZE/2)]
val_data = data[int(SIZE/2):int(3*SIZE//4)]
val_label = regression[int(SIZE/2):int(3*SIZE//4)]
test_data = data[int(3*SIZE//4):]
test_label = regression[int(3*SIZE//4):]

#print(labels[:100])
# As always, hyperparamters subject to optimatization
model = models.Sequential()
model.add(layers.Dense(84, activation='relu', input_shape=(84,)))
model.add(layers.Dense(3, activation='relu'))
model.add(layers.Dense(1))

model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

history = model.fit(partial_train, partial_label, shuffle=False, epochs=1000, batch_size=64, validation_data=(val_data, val_label))

#model.save('bench.h5')

results = model.evaluate(test_data, test_label)
print(results[1])
pred = model.predict(test_data)
# Error checking
#for i in range(len(pred)):
#	if pred[i] < 0.5 and test_label[i] == 1:
#		print("False Negative:", regression[i])


average_mae_history = history.history['val_mean_absolute_error']
tmae = history.history['mean_absolute_error']
# Plotting
a = plt.figure(1)
plt.plot(range(1, len(average_mae_history) + 1), average_mae_history, label="Validation")
plt.plot(range(1, len(tmae) + 1), tmae, label="Training")
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.legend()

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
plt.title("Smoothed")
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

a.show()
b.show()


plt.show()


