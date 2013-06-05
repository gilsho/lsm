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

def generateRandomMatrix(N):
	numcon = 50000  # numnber of connections in matrix
	Ar = [dict() for i in range(numcon)]
	for i in range(numcon):
		conn = Ar[i]
		conn[0] = int(np.random.random()*N)	#x1
		conn[1] = int(np.random.random()*N) #y1
		conn[2] = int(np.random.random()*N) #x2
		conn[3] = int(np.random.random()*N) #y2
		conn[4] = np.random.random()		#w
	return Ar

def generateTanyaMatrix2(N):
	ydiv = N/2
	conn_per_neuron = 14
	numcon = N*N*conn_per_neuron  # numnber of connections in matrix
	Ar = [dict() for i in range(numcon)]
	count = 0
	for i in range(N):
		for j in range(N):
			for k in range(conn_per_neuron):
				conn = Ar[count]
				count = count+1
				conn[0] = int(np.random.random()*N)	#x1
				yin = int(np.random.random()*N/2)
				if (k < conn_per_neuron/2):
					conn[1] = yin #y1
				else:
					conn[1] = yin+N/2
				conn[2] = int(i) #x2
				conn[3] = int(j) #y2
				if ((conn[0] <= ydiv and conn[2] <= ydiv) or
		    		(conn[0] > ydiv and conn[2] > ydiv)):
					conn[4] = 0.05
				else:
					conn[4] = -1
	return Ar

def generateTanyaMatrix(N):
	ydiv = N/2
	numcon = 5000  # numnber of connections in matrix
	Ar = [dict() for i in range(numcon)]
	for i in range(numcon):
		conn = Ar[i]
		conn[0] = int(np.random.random()*N)	#x1
		conn[1] = int(np.random.random()*N) #y1
		conn[2] = int(np.random.random()*N) #x2
		conn[3] = int(np.random.random()*N) #y2
		if ((conn[1] <= ydiv and conn[3] <= ydiv) or
		    (conn[1] > ydiv and conn[3] > ydiv)):
			conn[4] = 1
		else:
			conn[4] = -1
	return Ar

def setParams():
	N = 64
	sparsity_in = 8 # number of positions to skip
	n_inputs = 1
	Ain = np.random.random((n_inputs, N / sparsity_in, N / sparsity_in))
	#Ar = generateRandomMatrix(N)
	#Ar = generateTestMatrix(N)
	Ar = generateTanyaMatrix2(N)
	params = {'N':N, 
			  'sparsity_in':sparsity_in, 
			  'x0':[0.1, 0.0],
			  'tau':0.015, 
			  'tau_ref':0.001, 
			  'erev_e':[3.0, 2.5], 
			  'erev_i':[0.5, 0.5], 
			  'tau_syn':0.002,
			  'g_max':[10., 80.], 
			  'lam':[0.7, 0.1],
			  't_xmt':[0.001, 0.001],
			  'Ain':Ain, 'Ar':Ar}
	return params
