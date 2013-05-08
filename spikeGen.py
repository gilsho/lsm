# Input:
# file of times and spike rates
# file of connection weights
# Output:
# files of spike times for neurogrid drivers
import numpy as np
from setParams import setParams
# from matplotlib.pyplot import *
# from visualize import wavToArray

def generateSpikeTimes(times, rates):
	spk_times = []
	for i, rate in enumerate(rates[:-1]): # generate spike times
		t = times[i]
		while t < times[i+1]:
			if rate == 0.: # skip ahead to next rate 
				t = times[i+1]
			else: # generate spikes
				t = t + 1000. * np.random.exponential(1./rate)	# next spike time. 
				spk_times.append(t)
	return spk_times
	

def generateSpikes(filepath, params):
	# wav = wavToArray(filepath)
	# plot(wav)
	# show()
	rates = []
	times = []
	N = params['N']
	sparsity = params['sparsity']

	with open(filepath, 'r') as f: # read in designated spike rates
		for line in f:
			t, rate = line.split(' ')
			times.append(float(t))
			rates.append(float(rate))
	
	spk_times = generateSpikeTimes(times, rates)
	
	for y_targ in xrange(sparsity/2, N, sparsity): # generate file for each neuron in sparsity pattern
		for x_targ in xrange(sparsity/2, N, sparsity):
			# TODO, filter the spikes according to weights
			with open('./data/stim/training/y' + str(y_targ) + '_x' + str(x_targ) + '.txt', 'w') as f:
				for spk_time in spk_times:
					f.write(str(spk_time) + '\n')

params = setParams()
generateSpikes('./data/wav/wav1.dat', params)
