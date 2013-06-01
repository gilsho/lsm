#!/usr/bin/env python

# Input:
# file of times and spike rates
# file of connection weights
# Output:
# files of spike times for neurogrid drivers
import numpy as np
import os
import argparse
from setParams import setParams
# from matplotlib.pyplot import *
# from visualize import wavToArray

def generateSpikeTimes(durations, rates):
	spk_times = []
	t = 0.
	t_stop = 0.
	for i, rate in enumerate(rates): # generate spike times
		t_stop = t_stop + durations[i]
		while t < t_stop:
			if rate == 0.: # skip ahead to next rate 
				t = t_stop
			else: # generate spikes
				t = t + 1000. * np.random.exponential(1./rate)	# next spike time. 
				spk_times.append(t)
	return spk_times
	

def generateSpikes(filepath, params, exp_dir, ystart,yend):
	# wav = wavToArray(filepath)
	# plot(wav)
	# show()
	rates = []
	times = []
	N = params['N']
	sparsity_in = params['sparsity_in']
	Ain = params['Ain']

	with open(filepath, 'r') as f: # read in designated spike rates
		for line in f:
			t, rate = line.split(' ')
			times.append(float(t))
			rates.append(float(rate))
	
	spk_times = generateSpikeTimes(times, rates)
	
	for y_targ in xrange(ystart+sparsity_in, yend, sparsity_in): # generate file for each neuron in sparsity pattern
		for x_targ in xrange(sparsity_in/2, N, sparsity_in):
			y_idx = (y_targ - sparsity_in/2) / sparsity_in
			x_idx = (x_targ - sparsity_in/2) / sparsity_in
			w = Ain[0, x_idx, y_idx]
			with open(exp_dir + 'y' + str(y_targ) + '_x' + str(x_targ) + '.txt', 'w') as f:
				for spk_time in spk_times:
					if np.random.random() < w:
						delta = np.random.random()
						f.write(str(spk_time + delta) + '\n')

parser = argparse.ArgumentParser(description='Generate spikes')
parser.add_argument('exp_num', type=int, help='experiment number')
parser.add_argument('wavfile1', type=str, help='a wav file listing spike rates and durations')
parser.add_argument('wavfile2', type=str, help='a wav file listing spike rates and durations')
parser.add_argument('desc', type=str, help='brief description of experiment')
parser.add_argument('--seed', type=int, help='random number generator seed', default=1)
args = parser.parse_args()

np.random.seed(args.seed)

exp_num = args.exp_num
exp_dir = './data/exp' + str(exp_num) + '/';

d = os.path.dirname(exp_dir)
if not os.path.exists(d):
	os.makedirs(d)

params = setParams()
datadir = './data/wav/'
wavpath1 = datadir + args.wavfile1
wavpath2 = datadir + args.wavfile2
with open(exp_dir + 'README', 'w') as f:
	f.write(wavpath1 + ' ' + wavpath2 + ' ' + args.desc + '\n')
generateSpikes(wavpath1, params, exp_dir,0,params['N']/2)
generateSpikes(wavpath2, params, exp_dir,params['N']/2,params['N'])

