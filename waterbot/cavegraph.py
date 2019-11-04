'''
Version Notes
1.0: Made file, this demonstrates the ML vs existing FORTRAN/actual graph of cavity formation/hard sphere insertion

Version 1.0
11/4/2019
Owen Lockwood
'''

import numpy as np
import keras
from keras.models import load_model
from keras import models
import matplotlib.pyplot as plt
import math	


bin = 0.01
x_graph = np.zeros(shape=(int(0.5/bin)))

for i in range(len(x_graph)):
	x_graph[i] = i*bin+0.5*bin

y_act = np.zeros(shape=(int(0.5/bin)))
ML = np.zeros(shape=(int(0.5/bin)))
NUM_COORD = 33
SIZE = 500000
IN_FILE = "cave_skip_coord.dat"

all_data = np.zeros(shape=(SIZE, NUM_COORD))
all_labels = np.zeros(shape=(SIZE))
count = 0

with open(IN_FILE) as f:
	for line in f:
		if (count >= SIZE):
			break
		l = line.split('    ')
		l = l[1:]
		for i in range(len(l)):
			l[i] = float(l[i])
		all_data[count] = l[:NUM_COORD]
		all_labels[count] = l[NUM_COORD]
		count += 1

for i in range(SIZE):
	x = all_data[i][0]
	y = all_data[i][1]
	z = all_data[i][2]
	j = 3
	while (j < NUM_COORD):
		all_data[i][j] -= x
		all_data[i][j+1] -= y
		all_data[i][j+2] -= z
		j += 3
	all_data[i][0] = all_data[i][1] = all_data[i][2] = 0

td_data = np.zeros(shape=(SIZE, 10, 3))
for i in range(SIZE):
	j = 3
	while (j < NUM_COORD):
		td_data[i][int(j/3)-1][0] = all_data[i][j]
		td_data[i][int(j/3)-1][1] = all_data[i][j+1]
		td_data[i][int(j/3)-1][2] = all_data[i][j+2]
		j += 3

mlsum = 0
forsum = 0
for i in range(len(all_labels)):
	j = math.floor((all_labels[i])/bin)
	y_act[j] += 1
	forsum += 1	

#for i in range(len(y_act)):
	#y_act[i] /= 125000
	#y_act[i] *= 25
	#print(x_graph[i], y_act[i])

FORT = np.zeros(shape=(int(0.5/bin)))
with open("cave_skip.dat") as a:
	for line in a:
		l = line.split('  ')
		final = []
		#print("L ", l)
		for i in range(len(l)):
			l[i].strip()
			if (l[i] == '' or len(l[i]) == 2 or l[i] == '\n'): continue
			try:
				final.append(float(l[i]))
			except:
				print("ERROR ", l[i])		
		#print("Final ", final)
		FORT[math.floor((final[0])/bin)] = final[1]
#i = input()
model = load_model("cavemodel.h5")
pre = model.predict(td_data)
print(pre[0], len(pre))
for i in range(len(pre)):
	j = math.floor((pre[i])/bin)
	ML[j] += 1
	mlsum += 1

for i in range(len(ML)):
	ML[i] /= 125000
	ML[i] *= 25

#print(forsum, mlsum)
for i in range(len(FORT)):
	print(FORT[i], ML[i])
a = plt.figure(1)
plt.title("Traditional vs. Machine Learned Cavity Formation")
#plt.plot(x_graph, y_act, 'blue', label='Python')
plt.plot(x_graph, FORT, 'olive', label='FORTRAN')
plt.plot(x_graph, ML, 'red', label='ML')
plt.legend(loc='upper left')
plt.xlabel('Radius (nm)')
plt.ylabel('Prob')



a.show()

plt.show()




