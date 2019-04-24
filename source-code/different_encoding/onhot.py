# 0 is for Owen
# There are a variety of different combinations of the ways in which input can be represented, this is why part of this are commented out

import keras 
from keras import models
from keras import layers 
from keras.models import load_model
import numpy as np 
import matplotlib.pyplot as plt
import math
from keras.utils import plot_model

def vectorize_sequences(sequences, dimension=4050):
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

COORD = 63
# Files I have for my testing
#SIZE = 48206 #for coord.dat
#SIZE = 1887006 #for testcoord.dat
SIZE = 42812 #for nvtcoord.dat
BINARY = 63
'''
COORD = 84
SIZE = 296502
BINARY = 84
'''
data = np.zeros(shape=(SIZE,COORD))
labels = np.zeros(shape=SIZE, dtype=np.int64)
counter = 0
zero = 0
with open("nvtcoord.dat") as f:
	for line in f:	
		if counter >= SIZE:
			break
		l = line.split('   ')
		final = []
		l = l[1:]
		for i in range(len(l)):
			final.append(float(l[i]))		
		if final[BINARY] == 1 and counter < SIZE:
			labels[counter]= final[BINARY]
			data[counter] = final[:COORD]
			counter += 1
		elif final[BINARY] == 0 and counter < SIZE and zero < (SIZE/2):
			labels[counter] = final[BINARY]
			data[counter] = final[:COORD]
			counter += 1
			zero += 1


print(data[:3])
print(labels[:3])
'''
This changes the data to just have the nearest point. 
for i in range(len(data)):
	data[i][0] = x = data[i][0]
	data[i][1] = y = data[i][1]
	data[i][2] = z = data[i][2]
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
	data[i][3] = data[i][minj]
	data[i][4] = data[i][minj+1]
	data[i][5] = data[i][minj+2]
	j = 6
	while (j < len(data[i])):
		data[i][j] = 0
		j += 1
'''
# With the commenting the way that it is, this is a categorical encoding
print(data[:3])
print(labels[:3])
for j in range(len(data)):
	for k in range(len(data[j])):
		data[j][k] *= 1000

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
callback = [keras.callbacks.TensorBoard(log_dir='temp', histogram_freq=1, batch_size=256, write_graph=False, write_grads=False, \
    write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None, embeddings_data=None, update_freq='epoch')]
model = models.Sequential()
model.add(layers.Dense(32, activation='relu', input_shape=(4050,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(6, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(partial_train, partial_label, epochs=30, batch_size=128, validation_data=(val_data, val_label))

#plot_model(model, show_shapes=True, to_file='test.png')
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
#plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b')#, label='Validation acc')
#plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

a.show()
b.show()


plt.show()


