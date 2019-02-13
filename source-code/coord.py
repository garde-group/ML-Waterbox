# 0 is for Owen
'''
This program has a reliably >99% accuracy on test and validation, in it's current form it does overfit, but that can be easily fixed
by reducing the number of epochs.
'''
import keras 
from keras import models
from keras import layers 
import numpy as np 
import matplotlib.pyplot as plt

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
SIZE = 48206

data = np.zeros(shape=(SIZE,COORD))
labels = np.zeros(shape=SIZE, dtype=np.int64)
counter = 0
zero = 0
with open("coord.dat") as f:
	for line in f:	
		if counter >= SIZE:
			break
		l = line.split('   ')
		final = []
		l = l[1:]
		for i in range(len(l)):
			final.append(float(l[i]))	
		#final[COORD] should be changed, only works for 20 points not any other, I will update the changes later
		if final[COORD] == 1 and counter < SIZE:
			labels[counter]= final[COORD]
			data[counter] = final[:COORD]
			counter += 1
		elif final[COORD] == 0 and counter < SIZE and zero < (SIZE/2):
			labels[counter] = final[COORD]
			data[counter] = final[:COORD]
			counter += 1
			zero += 1
		
''' NORMALIZING DATA '''
''' 
for i in range(len(data)):
	for j in range(len(data[i])):
		dx = 0 - data[i][0] 
		dy = 0 - data[i][1]
		dz = 0 - data[i][2]
		if j % 3 == 0:
			data[i][j] += dx
		elif (j-1) % 3 == 0:
			data[i][j] += dy
		elif (j-2) % 3 == 0:
			data[i][j] += dz

'''

#print(data[:3])
#print(labels[:3])
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
model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(4050,)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(partial_train, partial_label, epochs=20, batch_size=512, validation_data=(val_data, val_label))

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



