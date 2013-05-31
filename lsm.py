import sys
sys.path.append("./lsm/")
import os
import numpy as np
import time
import setParams
import cPickle

def runExperiment(params, exp_dir):
	s0 = Soma("quadratic", {"tau_ref":params['tau_ref'], "tau":params['tau'], "x0":params['x0'][0]}) # Define a Soma model
	syn0e = Synapse("syn_generic", {"erev":params['erev_e'][0], "tau_syn":params['tau_syn'], "g_max":params['g_max'][0], "lambda":params['lam'][0], "t_xmt":params['t_xmt']})
	syn0i = Synapse("syn_generic", {"erev":params['erev_i'][0], "tau_syn":params['tau_syn'], "g_max":params['g_max'][0], "lambda":params['lam'][0], "t_xmt":params['t_xmt']})
	s0.AddSynapse(syn0e)
	s0.AddSynapse(syn0i)
	n0 = Neuron("reservoir", s0)
	p0 = Pool(n0, params['N'], params['N'])
	
	s1 = Soma("quadratic", {"tau_ref":params['tau_ref'], "tau":params['tau'], "x0":params['x0'][1]}) # Define a Soma model
	syn1e = Synapse("syn_generic", {"erev":params['erev_e'][1], "tau_syn":params['tau_syn'], "g_max":params['g_max'][1], "lambda":params['lam'][1], "t_xmt":params['t_xmt']})
	syn1i = Synapse("syn_generic", {"erev":params['erev_i'][1], "tau_syn":params['tau_syn'], "g_max":params['g_max'][1], "lambda":params['lam'][1], "t_xmt":params['t_xmt']})
	s1.AddSynapse(syn1e)
	s1.AddSynapse(syn1i)
	n1 = Neuron("connector", s1)
	p1 = Pool(n1, params['N'], params['N'])
	
	g = Group("LSM")
	g.AddChild(p0)
	g.AddChild(p1)
	
	g.VerticalProject(p0.Output(0),p1.Input(0))
	
	print 'Adding dummy horizontal connections\n'
	for i in range(params['N']):
		for j in range(params['N']):
			g.HorizontalProject(p1.Output(0),i,j,p0.Input(0),i,j,0.0)

	print 'Adding recurrent connections\n'
	for i in range(len(params['Ar'])):
		conn = params['Ar'][i]
		if con > 0:
			g.HorizontalProject(p1.Output(0), conn[0], conn[1], p0.Input(0), conn[2], conn[3],conn[4]) # p0.syne added first
		elif con < 0:
			g.HorizontalProject(p1.Output(0), conn[0], conn[1], p0.Input(1), conn[2], conn[3],conn[4]) # p0.syni added second
			
	print 'Adding stimulus\n'
	stim = []
	for y_targ in range(params['N']):
		for x_targ in range(params['N']):
			exi_stimfile = exp_dir + 'y' + str(y_targ) + '_x' + str(x_targ) + '.txt'
			if (os.path.exists(exi_stimfile)):	
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

reload(setParams)
exp_num = 2
params = setParams.setParams()
print 'tau_syn is:' + str(params['tau_syn'])
exp_dir = './lsm/data/exp' + str(exp_num) + '/';
d = os.path.dirname(exp_dir)
if not os.path.exists(d):
	print 'Experiment directory not found. Generate spikes first\n'
else:
	runExperiment(params, exp_dir)

