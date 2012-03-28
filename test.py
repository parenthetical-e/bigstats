def test_RHist():
	import numpy as np
	import scipy.stats as stats
	from bigstats.hist import RHist

	xs = stats.norm.rvs(size=10000)
	rh = RHist(name='test',decimals=1)
	[rh.incr(x) for x in xs]

	print('The normal distribution was sampled 10,000 times....')
	print('Est. Mean (0): {0}'.format(rh.mean()))
	print('Est. Var (1): {0}'.format(rh.var()))
	print('Est. Stdev (0.01): {0}'.format(rh.stdev()))
	print('N (10000): {0}'.format(rh.n()))
	print('** Decimals should be precise to 1 place.**')

	print('Plot 1 is frequencies, 2 is probabilites.')
	fig2 = rh.plot(fig=None,norm=True)

	# TODO: Add a uniform and some asymmetric dist too.