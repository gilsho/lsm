#!/usr/bin/env python

# file setting parameters for experiments
import numpy as np
import pdb

def generateTestMatrix(N):
	Ar = [dict() for i in range(N)]
	for i in range(N/2):
		conn = Ar[i]
		conn[0] = i
		conn[1] = i
		conn[2] = i
		conn[3] = i
		conn[4] = 1.0
		conn = Ar[i+N/2]
		conn[0] = i
		conn[1] = i
		conn[2] = i
		conn[3] = N-i
		conn[4] = 1.0
	return Ar

def generateReserviorMatrix(N):
	numcon = 100  # numnber of connections in matrix
	Ar = [dict() for i in range(numcon)]
	for i in range(numcon):
		conn = Ar[i]
		conn[0] = int(np.random.random()*N)	#x1
		conn[1] = int(np.random.random()*N) #y1
		conn[2] = int(np.random.random()*N) #x2
		conn[3] = int(np.random.random()*N) #y2
		conn[4]  = np.random.random()		#w
	return Ar

def setParams():
	N = 64
	sparsity_in = 16 # number of positions to skip
	n_inputs = 1
	Ain = np.random.random((n_inputs, N / sparsity_in, N / sparsity_in))
	#Ar = generateReserviorMatrix(N)
	Ar = generateTestMatrix(N)
	params = {'N':N, 
			  'sparsity_in':sparsity_in, 
			  'x0':[1.0,0.0],
			  'tau':0.015, 
			  'tau_ref':0.001, 
			  'erev':[2.5,3.0], 
			  'tau_syn':0.002,
			  'g_max':[80., 1.], 
			  'lam':[0.4,0.3],
			  't_xmt':0.005,
			  'Ain':Ain, 'Ar':Ar}
	return params
