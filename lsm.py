import sys
sys.path.append("./lsm/")
import os
import numpy as np
import time
from setParams import setParams
import cPickle

def runExperiment(params, exp_dir):
	s1 = Soma("quadratic", {"tau_ref":params['tau_ref'], "tau":params['tau'], "x0":params['x0'][0]}) # Define a Soma model
	syn1 = Synapse("syn_generic", {"erev":params['erev'][0], "tau_syn":params['tau_syn'], "g_max":params['g_max'][0], "lambda":params['lam'][0], "t_xmt":params['t_xmt']}) # Define a Synapse model
	s1.AddSynapse(syn1)
	n1 = Neuron("reservoir", s1)
	p1 = Pool(n1, params['N'], params['N'])
	
	s2 = Soma("quadratic", {"tau_ref":params['tau_ref'], "tau":params['tau'], "x0":params['x0'][1]}) # Define a Soma model
	syn2 = Synapse("syn_generic", {"erev":params['erev'][1], "tau_syn":params['tau_syn'], "g_max":params['g_max'][1], "lambda":params['lam'][1], "t_xmt":params['t_xmt']}) # Define a Synapse model
	s2.AddSynapse(syn2)
	n2 = Neuron("connector", s2)
	p2 = Pool(n2, params['N'], params['N'])
	
	g = Group("LSM")
	g.AddChild(p1)
	g.AddChild(p2)
	
	g.VerticalProject(p1.Output(0),p2.Input(0))
	
	print 'Adding dummy horizontal connections\n'
	for i in range(params['N']):
		for j in range(params['N']):
			g.HorizontalProject(p2.Output(0),i,j,p1.Input(0),i,j,0.0)

	print 'Adding recurrent connections\n'
	for i in range(len(params['Ar'])):
		conn = params['Ar'][i]
		g.HorizontalProject(p2.Output(0), conn[0], conn[1], 
							p1.Input(0), conn[2], conn[3],conn[4]) 
	
	print 'Adding stimulus\n'
	stim = []
	for y_targ in xrange(params['sparsity_in']/2, params['N'], params['sparsity_in']):
		for x_targ in xrange(params['sparsity_in']/2, params['N'], params['sparsity_in']):
			exi_stimfile = exp_dir + 'y' + str(y_targ) + '_x' + str(x_targ) + '.txt'
			stim.append(Stimulus(SpikeSource("file_generator", {'filename':exi_stimfile})))
			p1.AddStimulus(stim[-1], 0)
			stim[-1].AddTarget(x_targ, y_targ)

	SetSavePath(exp_dir + 'out')
	print 'Saving to ' + exp_dir + 'out\n'
	MapNetwork(g)
	time.sleep(5)
	print 'Starting Experiment'
	StartExp()
	time.sleep(10)
	StopExp()
	print 'Done'

exp_num = 1
params = setParams()
print 'tau_syn is:' + str(params['tau_syn'])
exp_dir = './lsm/data/exp' + str(exp_num) + '/';
d = os.path.dirname(exp_dir)
if not os.path.exists(d):
	print 'Experiment directory not found. Generate spikes first\n'
else:
	runExperiment(params, exp_dir)

