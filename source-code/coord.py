# 0 is for Owen
'''
This program has a reliably >99% accuracy on test and validation, in it's current form it does overfit, but that can be easily fixed
by reducing the number of epochs. This is the one hot encoded/categorically encoded version. 
'''
import keras 
from keras import models
from keras import layers 
from keras.models import load_model
import numpy as np 
import matplotlib.pyplot as plt

# The custiom categorical function, encodes into 4050 dimension
def vectorize_sequences(sequences, dimension=4050):
	results = np.zeros((len(sequences), dimension))
	for i in range(len(sequences)):
		for j in range(len(sequences[i])):
			results[i][int(sequences[i][j])] = 1
	return results

# Custom shuffling function
def every_day_im_shuffling(a, b):
	rng_state = np.random.get_state()
	np.random.shuffle(a)
	np.random.set_state(rng_state)
	np.random.shuffle(b)

# Number of coordinates
COORD = 63
# The total size of the coordinates
SIZE = 48206

# Set the input data and labels to zero
data = np.zeros(shape=(SIZE,COORD))
labels = np.zeros(shape=SIZE, dtype=np.int64)
counter = 0
zero = 0
# Open the file and load in the data
with open("coord.dat") as f:
	for line in f:	
		if counter >= SIZE:
			break
		l = line.split('   ')
		final = []
		l = l[1:]
		for i in range(len(l)):
			final.append(float(l[i]))	
        # Load in equal amounts of 1s and 0s to ensure optimal binary classification training	
		if final[63] == 1 and counter < SIZE:
			labels[counter]= final[63]
			data[counter] = final[:63]
			counter += 1
		elif final[63] == 0 and counter < SIZE and zero < (SIZE/2):
			labels[counter] = final[63]
			data[counter] = final[:63]
			counter += 1
			zero += 1
		
''' NORMALIZING DATA '''
''' 
This is unecessary to do, but it was a testing thing
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

# Scale everything up to be placed in vector
for j in range(len(data)):
	for k in range(len(data[j])):
		data[j][k] *= 1000

every_day_im_shuffling(data, labels) 
data = vectorize_sequences(data)
#Split the data and labels in a simple hold validation pattern, 1/2 train, 1/4 validation, 1/4 test
# This can definitely be changed and improved
partial_train = data[:int(SIZE/2)]
partial_label = labels[:int(SIZE/2)]
val_data = data[int(SIZE/2):int(3*SIZE//4)]
val_label = labels[int(SIZE/2):int(3*SIZE//4)]
test_data = data[int(3*SIZE//4):]
test_label = labels[int(3*SIZE//4):]
num_1 = 0
num_0 = 0
#print(labels[:100])
# This is just to ensure that the correct number of ones and zeros are occuring
for i in partial_label:
	if i == 0:
		num_0 += 1
	elif i == 1:
		num_1 += 1

print("num 1:", num_1, "num 0:", num_0)
# Simple densly connected model, this can definitely be optimized
model = models.Sequential()
# The number of nodes can be changes
model.add(layers.Dense(16, activation='relu', input_shape=(4050,)))
model.add(layers.Dense(8, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(partial_train, partial_label, epochs=20, batch_size=512, validation_data=(val_data, val_label))
# Save the model to be able to be reloaded and used/tested
model.save('bench.h5')

#evaluate the testing data
results = model.evaluate(test_data, test_label)
print(results[1])
history_dict = history.history
history_dict.keys()

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

# Make a graph of the training and validation losses and accuracies
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
