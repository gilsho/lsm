import numpy
width = 64
height = 64
sparsity = 8
p = .125

syn2 = Synapse("cond_syn", {"g_max":0.2,"erev": 2.5})
arb2 = Arbor("arbor", {"lambda": .1}, syn2)
syn3 = Synapse("cond_syn", {"g_max":0.2,"erev": 0.5})
arb3 = Arbor("arbor", {"lambda": .1}, syn3)
s2 = Soma("quadratic", {"tau_ref": 0.015, "tau": 15e-3, "x0": .0})
s2.AddArbor(arb2)
s2.AddArbor(arb3)
n2 = Neuron("tgt_pool", s2)

s1 = Soma("quadratic", {"tau_ref": 0.015, "tau": 15e-3, "x0": .0})
n1 = Neuron("src_pool", s1)                    
p1 = Pool(n1, width, height)

p2 = Pool(n2, width, height)

g = Group()
g.AddChild(p1)

a = numpy.array([[-1.0 for i in range(0,(width*height))] for j in range(0,((width*height/sparsity)/sparsity/2))] + [[1.0 for i in range(0,(width*height))] for j in range(0,((width*height/sparsity)/sparsity/2))])
#print(a[(240,240)])
#b = CreateWeightMatrix(a)
g.NEFProjection(p1.Output(0), p2.Input(0), 0, 0, a, sparsity)

MapNetwork(g)

SetSavePath('~/lsm/
StartExp()
sleep(time)
StopExp()
