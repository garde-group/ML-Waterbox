import keras 
from keras import models
from keras import layers 
from keras.models import load_model
import numpy as np 
import time 

def vectorize_sequences(sequences, dimension=4050):
	results = np.zeros((len(sequences), dimension))
	for i in range(len(sequences)):
		for j in range(len(sequences[i])):
			results[i][int(sequences[i][j])] = 1
	return results

SIZE = 12052
COORD = 63
data = np.zeros(shape=(SIZE,COORD))
labels = np.zeros(shape=SIZE, dtype=np.int64)
counter = 0
with open("b.dat") as f:
    for line in f:
        l = line.split(' ')
        final = []
        for i in range(len(l)): 
            final.append(float(l[i]))	
        if final[63] == 1:
            labels[counter] = final[63]
            data[counter] = final[:63]
            counter += 1
        elif final[63] == 0:
            labels[counter] = final[63]
            data[counter] = final[:63]
            counter += 1
        

#print(data[:3], labels[:3])
for j in range(len(data)):
	for k in range(len(data[j])):
		data[j][k] *= 1000
data = vectorize_sequences(data)
model = load_model("bench.h5")
start = time.time()
results = model.evaluate(data, labels)
end = time.time()
predictions = []
np.set_printoptions(threshold=5000)
start1 = time.time()
predictions = model.predict(data)
end1 = time.time()
ones = 0
zeros = 0
for i in predictions:
    if i < 0.5:
        zeros += 1
    elif i > 0.5 :
        ones += 1
    else:
        print(i)

print("Time of evaluation:", end-start, "Accuracy:", results[1])
print("Time of predictions:", end1-start1, "Num 0:", zeros, "Num 1:", ones)
