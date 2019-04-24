# 0 is for Owen
# This program trains a network on the box fortran code output
# Check the encodings folder for more of these sort of codes
# This one doesn't work super well, and functions fundamentally similar to the coord.py
import keras 
from keras import models
from keras import layers 
from keras.models import load_model
import numpy as np 
import matplotlib.pyplot as plt

def vectorize_sequences(sequences, dimension=4000):
	results = np.zeros((len(sequences), dimension))
	for i in range(len(sequences)):
		for j in range(len(sequences[i])):
			results[i][int(sequences[i][j])] = 1
	return results

def every_day_im_shuffling(a, b):
	rng_state = np.random.get_state()
	np.random.shuffle(a)
	np.random.set_state(rng_state)
	np.random.shuffle(b)

COORD = 84
SIZE = 604210
BINARY = 84
# These are for the binary classification and for the regression lables
R = 82

data = np.zeros(shape=(SIZE,COORD))
labels = np.zeros(shape=SIZE, dtype=np.int64)
counter = 0
zero = 0
# Reading in the file, the size restrictions are only for binary classification and can be removed for regression
with open("btest2.dat") as f:
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
			counter += 1
		elif final[BINARY] == 0 and counter < SIZE and zero < (SIZE/2):
			labels[counter] = final[BINARY]
			data[counter] = final[:BINARY]
			counter += 1
			zero += 1
		#print(data[counter])

print(data[:3])
print(labels[:3])

for j in range(len(data)):
	for k in range(len(data[j])):
		data[j][k] *= 1000

# Shuffle, encode, then split
every_day_im_shuffling(data, labels) 
data = vectorize_sequences(data)
partial_train = data[:int(SIZE/2)]
partial_label = labels[:int(SIZE/2)]
val_data = data[int(SIZE/2):int(3*SIZE//4)]
val_label = labels[int(SIZE/2):int(3*SIZE//4)]
test_data = data[int(3*SIZE//4):]
test_label = labels[int(3*SIZE//4):]
num_1 = 0
num_0 = 0
#print(labels[:100])
for i in partial_label:
	if i == 0:
		num_0 += 1
	elif i == 1:
		num_1 += 1

print("num 1:", num_1, "num 0:", num_0)
# Train then graph the results
model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(4000,)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(partial_train, partial_label, epochs=20, batch_size=512, validation_data=(val_data, val_label))

#model.save('bench.h5')

results = model.evaluate(test_data, test_label)
print(results[1])
history_dict = history.history
history_dict.keys()

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)
a = plt.figure(1)
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

b = plt.figure(2)
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

a.show()
b.show()


plt.show()


