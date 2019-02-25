import numpy as np 

COORD = 63
SIZE = 48206

def every_day_im_shuffling(a, b):
	rng_state = np.random.get_state()
	np.random.shuffle(a)
	np.random.set_state(rng_state)
	np.random.shuffle(b)

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
		if final[63] == 1 and counter < SIZE:
			labels[counter] = final[63]
			data[counter] = final[:63]
			counter += 1
		elif final[63] == 0 and counter < SIZE and zero < (SIZE/2):
			labels[counter] = final[63]
			data[counter] = final[:63]
			counter += 1
			zero += 1

every_day_im_shuffling(data, labels) 
output_data = data[int(3*SIZE//4):]
output_label = labels[int(3*SIZE//4):]

with open("b.dat", "w") as b:
	for i in range(len(output_data)):
		out = list(output_data[i])
		out = ' '.join(str(k) for k in out)
		out = str(out)
		out = out + " " + str(output_label[i]) + "\n"
		b.write(out)

with open("bf.dat", "w") as b:
	for i in range(len(output_data)):
		for j in range(len(output_data[i])):
			out = str(output_data[i][j])
			out += '\n'
			b.write(out)
		out = str(labels[i])
		out += '\n'
		b.write(out)
