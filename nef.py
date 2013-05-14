import sys
sys.path.append("./lsm/")
import os
import numpy
import time
from setParams import setParams

def runExperiment(params, exp_dir):
	s1 = Soma("quadratic", {"tau_ref":params['tau_ref'], "tau":params['tau'], "x0":params['x0']}) # Define a Soma model
	syn1 = Synapse("syn_generic", {"erev":params['erev'], "tau_syn":params['tau_syn'], "g_max":params['g_max'], "lambda":params['lam'], "t_xmt":params['t_xmt']}) # Define a Synapse model
	s1.AddSynapse(syn1)
	n1 = Neuron("reservoir", s1)
	p1 = Pool(n1, params['N'], params['N'])
	
	g = Group("LSM")
	g.AddChild(p1)
	
	# a = numpy.array([[-1.0 for i in range(0,(width*height))] for j in range(0,((width*height/sparsity)/sparsity/2))] + [[1.0 for i in range(0,(width*height))] for j in range(0,((width*height/sparsity)/sparsity/2))])
	#print(a[(240,240)])
	#b = CreateWeightMatrix(a)
	# g.NEFProjection(p1.Output(0), p2.Input(0), 0, 0, a, sparsity)
	
	stim = []
	for y_targ in xrange(params['sparsity']/2, params['N'], params['sparsity']):
		for x_targ in xrange(params['sparsity']/2, params['N'], params['sparsity']):
			exi_stimfile = exp_dir + 'y' + str(y_targ) + '_x' + str(x_targ) + '.txt'
			stim.append(Stimulus(SpikeSource("file_generator", {'filename':exi_stimfile})))
			p1.AddStimulus(stim[-1], 0)
			stim[-1].AddTarget(x_targ, y_targ)
	
	
	# exi_stimfile = 'test.txt'
	# stim.append(Stimulus(SpikeSource("file_generator", {'filename':exi_stimfile})))
	# p1.AddStimulus(stim[-1], 0)
	# stim[-1].AddTarget(12, 12)

	SetSavePath(exp_dir + 'out')
	print 'Saving to ' + exp_dir + 'out\n'
	MapNetwork(g)
	time.sleep(5)
	StartExp()
	time.sleep(10)
	StopExp()

exp_num = 1
params = setParams()
exp_dir = './lsm/data/exp' + str(exp_num) + '/';
d = os.path.dirname(exp_dir)
if not os.path.exists(d):
	print 'Experiment directory not found. Generate spikes first\n'
else:
	runExperiment(params, exp_dir)

