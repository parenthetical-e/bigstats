""" A class for calculating histograms incrementally. """
from collections import defaultdict
import numpy as np

class RHist():
	""" 
	Creates histogram/bins where the bin size and location is set by 
	rounding (i.e.<decimals>) but where the number and range of bins 
	is determined online. 

	As a result you need only know in advance the approximate scale 
	your data will take, i.e. the precision you're interested in.

	<decimals> is an integer specifying the number of decimals places.
	Negative numbers behave as expected. For more information on 
	<decimals> see the docs for numpy.round().  
	"""

	def __init__(self,decimals=1):
		self.decimals = decimals
		self.h = defaultdict(int)

		self.h_norm = None


	def incr(self,x):
		self.h[np.round(x,self.decimals)] += 1


	def norm(self):
		""" Calculate the normalized histogram (i.e. a PMF). """
		from copy import deepcopy
		# Borrowed from the implementation discussed in 
		# Think Stats Probability and Statistics for Programmers
		# By Allen B. Downey, p 16.
		# http://shop.oreilly.com/product/0636920020745.do
		
		self.h_norm = deepcopy(self.h)

		weight = 1./self.n()
		for k in self.h_norm.keys():
			self.h_norm[k] *= weight


	def mean(self):
		""" Estimate and return the mean. """
		# Borrowed from the implementation discussed in 
		# Think Stats Probability and Statistics for Programmers
		# By Allen B. Downey, p 16.
		# http://shop.oreilly.com/product/0636920020745.do

		if self.h_norm is None:
			self.norm()

		mean = 0.0
		for x, p in self.h_norm.items():

			# mean = sum_i(p_i*x_i)
			mean += p * x
		
		return mean


	def var(self):
		""" Estimate and return the variance. """
		# Borrowed from the implementation discussed in 
		# Think Stats Probability and Statistics for Programmers
		# By Allen B. Downey, p 16.
		# http://shop.oreilly.com/product/0636920020745.do

		if self.h_norm is None:
			self.norm()

		# var = sum_i(p_i * (x_i - mean)*2)
		mean = self.mean()
		var = 0.0
		for x, p in self.h_norm.items():
			var += p * (x - mean) ** 2
		
		return var

		
	def n(self):
		""" Count and return the total number of samples """

		return np.sum(self.h.values())


	def fitPDF(self,family):
		""" Fit a probability density function (of type <family>) """

		# TODO
		pass


	def plot(self,pid=None,norm=True):
		"""
		Plot the histogram.  

		If provided current data is added to <pid>, a matplotlib plot 
		identifier.  
		<norm> indicates whether the raw counts or normalized values 
		should be plotted.
		"""

		if norm:
			if self.h_norm is None:
				self.norm()
			
		# TODO
		pass


class Hist(RHist):
	""" A histogram/bin class with a known <min>, <max> with <num> of bins """ 
	
	def __init__(self,min,max,num):
		try: RHist.__init__(self)
		except AttributeError: pass

		# TODO create bins for self.h	
		pass


	def incr(self,x):
		# TODO overide
		pass	
