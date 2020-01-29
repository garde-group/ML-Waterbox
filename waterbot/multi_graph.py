'''
Version Notes
1.0: Made file, this demonstrates the ML vs existing FORTRAN/actual graph of q 

Version 1.0
1/28/2020
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
ML_cav = np.zeros(shape=(int(0.5/bin)))
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
cav_labels = np.zeros(shape=(SIZE))
for i in range(SIZE):
	j = 3
	while (j < NUM_COORD):
		td_data[i][int(j/3)-1][0] = all_data[i][j]
		td_data[i][int(j/3)-1][1] = all_data[i][j+1]
		td_data[i][int(j/3)-1][2] = all_data[i][j+2]
		j += 3
	dist = 10
	for k in range(4):
		dx = abs(td_data[i][k][0])
		if dx > 2.5:
			dx -= 5
		dy = abs(td_data[i][k][1])
		if dy > 2.5:
			dy -= 5
		dz = abs(td_data[i][k][2])
		if dz > 2.5:
			dz -= 5
		temp = math.sqrt(dx**2 + dy**2 + dz**2)
		if temp < dist:
			dist = temp
	cav_labels[i] = dist
	if dist > 1:
		print(dist, td_data[i])


FORT = np.zeros(shape=(int(2/bin)))
FORT_cav = np.zeros(shape=(int(0.5/bin)))
for i in cav_labels:
	FORT_cav[int(math.floor(i/bin))] += 1
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
		try:
			FORT[int(math.floor((final[0]+1)/bin))] = final[1]
		except:
			print("ERROR IN ADDING TO LIST:", final[0])

model = load_model("multi_head_cave.h5")
pre = model.predict(td_data)
results = model.evaluate(td_data, [cav_labels, all_labels])
#print(pre[0], len(pre))
for i in range(len(pre[1])):
	j = math.floor((pre[1][i]+1)/bin)
	if (j >= 200):
		#print("HERE", j)
		#continue		
		j = 199
	ML[int(j)] += 1

for i in range(len(ML)):
	ML[i] /= 4142.

for i in range(len(pre[0])):
	j = int(math.floor((pre[0][i])/bin))
	try:
		ML_cav[j] += 1
	except:
		pass
		#print("error", j)


for i in range(len(ML_cav)):
	FORT_cav[i] /= 4142
	FORT_cav[i] /= 5
	#FORT_cav[i] *= 25
	ML_cav[i] /= 4142
	ML_cav[i] /= 5
	#ML_cav[i] *= 25
print(len(cav_labels), len(pre[0]))

a = plt.figure(1)
plt.title("Traditional vs. Machine Learned TOP")
plt.plot(x_graph, FORT, 'olive', label='Actual')
plt.plot(x_graph, ML, 'red', label='ML')
plt.legend(loc='upper left')
plt.xlabel('q')
plt.ylabel('Prob')

x_graph_cav = np.zeros(shape=(int(0.5/bin)))

for i in range(len(x_graph_cav)):
	x_graph_cav[i] = i*bin+0.5*bin


d = plt.figure(4)
plt.title("Traditional vs. Machine Learned Cavity Formation")
plt.plot(x_graph_cav, FORT_cav, 'olive', label='Actual')
plt.plot(x_graph_cav, ML_cav, 'red', label='ML')
plt.legend(loc='upper right')
plt.xlabel('Radius (nm)')
plt.ylabel('Prob')



'''
heat_pre = model.predict(heat_data)
# heat map actual
b = plt.figure(2)
plt.scatter(heat_y, heat_z, s=100, c=ss_label, cmap="hot", vmin=0, vmax=1, alpha=0.9)
plt.colorbar()
plt.xlabel("y axis")
plt.ylabel("z axis")
plt.title("Actual")


# heat map ML
c = plt.figure(3)
plt.scatter(heat_y, heat_z, s=100, c=heat_pre, cmap="hot", vmin=0, vmax=1, alpha=0.9)
plt.colorbar()
plt.xlabel("y axis")
plt.ylabel("z axis")
plt.title("ML")

'''
a.show()
'''
b.show()
c.show()
'''
d.show()
plt.show()



