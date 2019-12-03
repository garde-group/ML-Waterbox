'''
Version Notes
1.0: Made file, this demonstrates the ML vs existing FORTRAN/actual graph of q 
1.1: Added heatmap functionality (likely still in process)
1.2: Added Colorbars to heatmaps
1.3: Properly lined up colorbars

Version 1.3
12/3/2019
Owen Lockwood
'''

import numpy as np
import keras
from keras.models import load_model
from keras import models
import matplotlib.pyplot as plt
import math	


bin = 0.01
x_graph = np.zeros(shape=(int(2/bin)))

for i in range(len(x_graph)):
	x_graph[i] = i*bin-1+0.5*bin

y_act = np.zeros(shape=(int(2/bin)))
ML = np.zeros(shape=(int(2/bin)))
NUM_COORD = 15
SIZE = 414200
IN_FILE = "tetra_skip_coord.dat"

all_data = np.zeros(shape=(SIZE, NUM_COORD))
all_labels = np.zeros(shape=(SIZE))

count = 0

with open(IN_FILE) as f:
	for line in f:
		if (count >= SIZE):
			break
		l = line.split('    ')
		l = l[1:]
		l[15] = l[15].strip()		
		for i in range(len(l)):
			l[i] = float(l[i])
		all_data[count] = l[:NUM_COORD]
		all_labels[count] = l[NUM_COORD]
		count += 1
ss = []
ss_label = []
nn_heat = []
for i in range(4142):
	if all_data[i][0] < 2.6 and all_data[i][0] > 2.4:
		ss.append([all_data[i][1], all_data[i][2]])
		ss_label.append(all_labels[i])
		nn_heat.append(all_data[i])
		
s = len(ss)
ss = np.asarray(ss)
#print("SIZE :", s, ss.shape, ss)
nn_heat = np.asarray(nn_heat)
ss = np.swapaxes(ss, 0, 1)
#print("SIZE :", s, ss.shape, ss)
heat_y = ss[0]
heat_z = ss[1]

for i in range(len(nn_heat)):
	x = nn_heat[i][0]
	y = nn_heat[i][1]
	z = nn_heat[i][2]
	j = 3
	while (j < NUM_COORD):
		nn_heat[i][j] -= x
		nn_heat[i][j+1] -= y
		nn_heat[i][j+2] -= z
		j += 3
	nn_heat[i][0] = nn_heat[i][1] = nn_heat[i][2] = 0
heat_data = np.zeros(shape=(s, 4, 3))
for i in range(s):
	j = 3
	while (j < NUM_COORD):
		heat_data[i][int(j/3)-1][0] = nn_heat[i][j]
		heat_data[i][int(j/3)-1][1] = nn_heat[i][j+1]
		heat_data[i][int(j/3)-1][2] = nn_heat[i][j+2]
		j += 3

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

td_data = np.zeros(shape=(SIZE, 4, 3))
for i in range(SIZE):
	j = 3
	while (j < NUM_COORD):
		td_data[i][int(j/3)-1][0] = all_data[i][j]
		td_data[i][int(j/3)-1][1] = all_data[i][j+1]
		td_data[i][int(j/3)-1][2] = all_data[i][j+2]
		j += 3

#for i in range(len(all_labels)):
	#j = math.floor((all_labels[i]+1)/bin)
	#y_act[j] += 1

#for i in range(len(y_act)):
	#y_act[i] /= 4142.
	#print(x_graph[i], y_act[i])

FORT = np.zeros(shape=(int(2/bin)))
with open("tetra_skip.dat") as a:
	for line in a:
		l = line.split('   ')
		final = []
		for i in range(len(l)):
			l[i].strip()
			if (l[i] == '' or len(l[i]) == 2): continue
			try:
				final.append(float(l[i]))
			except:
				print(len(l[i]))		
		#print(final)
		FORT[int(math.floor((final[0]+1)/bin))] = final[1]

model = load_model("tetramodelconv.h5")
pre = model.predict(td_data)
#print(pre[0], len(pre))
for i in range(len(pre)):
	j = math.floor((pre[i]+1)/bin)
	if (j >= 200):
		print("HERE", j)
		j = 199
	ML[int(j)] += 1

for i in range(len(ML)):
	ML[i] /= 4142.


heat_pre = model.predict(heat_data)

a = plt.figure(1)
#plt.plot(x_graph, y_act, 'blue', label='Python')
plt.plot(x_graph, FORT, 'olive', label='FORTRAN')
plt.plot(x_graph, ML, 'red', label='ML')
plt.legend(loc='upper left')
plt.xlabel('q')
plt.ylabel('Prob')

# heat map actual
b = plt.figure(2)
plt.scatter(heat_y, heat_z, s=100, c=ss_label, cmap="hot", vmin=0, vmax=1, alpha=0.9)
plt.colorbar()
plt.xlabel("y axis")
plt.ylabel("z axis")
plt.title("Actual")


# heat map ML
c = plt.figure(3)
plt.scatter(heat_y, heat_z, s=100, c=heat_pre, cmap="hot", vmin=0, vamx=1, alpha=0.9)
plt.colorbar()
plt.xlabel("y axis")
plt.ylabel("z axis")
plt.title("ML")


a.show()
b.show()
c.show()

plt.show()



