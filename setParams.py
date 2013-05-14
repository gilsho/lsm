#!/usr/bin/env python

# file setting parameters for experiments
import numpy as np

def setParams():
	N = 64
	sparsity = 16
	n_inputs = 1
	Ain = np.random.random((n_inputs, N / sparsity, N / sparsity))
	print "input weights:\n" + str(Ain)
	params = {'N':N, 
			  'sparsity':sparsity, 
			  'x0':0.0,
			  'tau':0.01, 
			  'tau_ref':0.005, 
			  'tau_syn':.01, 
			  'erev':3.0, 
			  'g_max':1, 
			  'lam':0.4,
			  't_xmt':0.005,
			  'Ain':Ain}
	return params
