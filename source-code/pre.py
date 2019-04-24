# 0 is for Owen
'''
This is a simple program the reads how many ones and zeros there are, which is meant to be used after running the fortran code but before
the training. This really should and could be integrated into the fortran code, but I just never got around to doing that
'''
import numpy as np

COORD = 63
# Total size of all the outputs
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
#print(labels[:100])\
# Count the total number ones and zeros to be able to get the accurate size for the coord.py
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
