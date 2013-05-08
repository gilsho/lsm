# file setting parameters for experiments
import numpy as np

def setParams():
	N = 32
	sparsity = 8
	n_inputs = 1
	Ain = np.random.random((n_inputs, N**2 / sparsity**2))
	params = {'N':32, 'sparsity':8, 'Ain':Ain}
	return params
