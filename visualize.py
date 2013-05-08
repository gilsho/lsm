
import numpy as np
from matplotlib.pyplot import *

def wavToArray(filepath):
	f = open(filepath, 'r')
	wav = np.zeros(0)
	val = 0
	for line in f:
		print "line is: " + line
		t, newval = line.split(' ')
		addwav = np.ones(int(t)-len(wav))*val
		wav = np.append(wav,addwav)
		val = float(newval)
	return wav


# plot(wavToArray('./dat/wav/wav1.dat')); show()




