import cPickle

syn2 = Synapse("syn_generic", {"erev": .1})
s2 = Soma("quadratic", {"tau_ref": 1e-3, "tau": 15e-3, "x0": .01, "g_inf": 6.})
s2.AddSynapse(syn2)
n2 = Neuron("src_nrn", s2)

syn1 = Synapse("syn_generic", {"erev": .1})
s1 = Soma("quadratic", {"tau_ref": 1e-3, "tau": 15e-3, "x0": .01, "g_inf": 6.})
s1.AddSynapse(syn1)
n1 = Neuron("tgt_nrn", s1)

p1 = Pool(n1, 128, 128)
p2 = Pool(n2, 128, 128)

g = Group()
g.AddChild(p1)
g.AddChild(p2)

g.VerticalProject(p1.Output(0), p2.Input(0))

for x in range(0, 128, 2):
	for y in range(0, 128, 2):
		if y>64:
			g.HorizontalProject(p2.Output(0), x, y, p1.Input(0), x, y, 1.0)
			g.HorizontalProject(p2.Output(0), x, y, p1.Input(0), x + 1, y + 1, 1.0)
		else:
			g.HorizontalProject(p2.Output(0), x, y, p1.Input(0), x, y, 0.0)
			g.HorizontalProject(p2.Output(0),x,y,p1.Input(0), x+1, y+1, 0.0)
MapNetwork(g)
