# file setting parameters for experiments
import numpy as np

def setParams():
	N = 32
	sparsity = 8
	n_inputs = 1
	Ain = np.random.random((n_inputs, N / sparsity, N / sparsity))
	print "input weights:\n" + str(Ain)
	params = {'N':32, 'sparsity':8, 'Ain':Ain}
	return params
