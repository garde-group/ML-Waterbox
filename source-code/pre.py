import numpy as np

COORD = 63
SIZE = 640000


data = np.zeros(shape=(SIZE,COORD))
labels = np.zeros(shape=SIZE, dtype=np.int64)
counter = 0
zero = 0
with open("coord.dat") as f:
	for line in f:	
		if counter >= SIZE:
			pass
			#break
		l = line.split('   ')
		final = []
		l = l[1:]
		for i in range(len(l)):
			final.append(float(l[i]))	
		if final[COORD] == 1:
			labels[counter]= final[COORD]
			data[counter] = final[:COORD]
			counter += 1
		elif final[COORD] == 0:
			labels[counter] = final[COORD]
			data[counter] = final[:COORD]
			counter += 1
			zero += 1

num_1 = 0
num_0 = 0
#print(labels[:100])
for i in labels:
	if i == 0:
		num_0 += 1
	elif i == 1:
		num_1 += 1
print("num 1:", num_1, "num 0:", num_0)
t = []
for i in range(len(data)):
	t.append(np.amax(data[i]))

print(max(t))	
