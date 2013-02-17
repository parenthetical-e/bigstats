""" A class for building histograms incrementally. """
import numpy as np
from collections import defaultdict


class RHist():
    """ 
    A class for calculating histograms where the bin size 
    and location is set by rounding the input (i.e. use <decimals>) but 
    where the number and range of bins is determined by the data. 
    
    As a result, you need only know in advance the approximate scale 
    your data will take, i.e. the precision you're interested in.

    There are a few methods that return useful statistics.

    <name> is a unique identifier for this histogram.

    <decimals> is an integer specifying the number of decimal places.
    Negative numbers behave as expected.  
    """

    def __init__(self,name,decimals=1):
        self.decimals = decimals
        self.name = name

        self.h = defaultdict(int)
        self.h_norm = None


    def add(self,x):
        """ Add <x>, a data point, to the histogram """

        # Do type checking here?
        self.h[np.round(x,self.decimals)] += 1


    def norm(self):
        """ 
        Calculate the normalized histogram (i.e. a probability
        mass function). 
        """
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
    
    
    def median(self):
        """ Estimate and return the median. """
        
        # Get all the key values
        # and sort them.
        values = self.h.keys()
        values = sorted(values)
        
        # And count them too
        nvalues = len(values)

        # If even:
        if (nvalues % 2) == 0:
            median = (values[nvalues / 2] + values[(nvalues / 2) + 1]) / 2.0
        # Or odd
        else:
            median = values[(nvalues + 1) / 2]
        
        return median
    
    
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
        """ Count and return the total number of samples. """

        return np.sum(self.h.values())


    def stdev(self):
        """ Estimate and return the variance. """

        var = self.var()
        n = self.n()

        return np.sqrt(var/(n-1))


    def se(self):
        """ Estimate and return the standard error. """
        
        sd = self.stdev()
        n = self.n()
        
        return sd / np.sqrt(n)


    def above(self, criterion):
        """ Estimate and return the percent area of the histogram at 
        or above the <criterion>. """
        
        # If the bin is at or above, add to the list of values
        # the sum and norm the values.
        values = [value for key, value in self.h.items() if key >= criterion]
        
        return np.sum(values) / float(self.n())


    def overlap(self, Rhist):
        """ Calculates the percent overlap between this histogram and 
        <Rhist>, another histogram instance. 
        
        Note: percent overlap is calculated by finding the difference
        in absolute counts for all overlapping bins, summing these, 
        then normalizing by the total counts for both distributions
        (all bins). """
        
        n1 = self.n()  ## Get total counts
        n2 = Rhist.n()
        
        # Tabulate the diffs for each
        # overlapping bin.
        diffs = []
        for key, val1 in self.h.items():
            try:
                val2 = Rhist.h[key]
            except KeyError:
                pass
            else:
                val1 = float(val1)
                val2 = float(val2)
                diffs.append(max(val1, val2) - np.abs(val1 - val2))
        
        # Sum, then normalize by total count.
        return np.sum(diffs) / (n1 + n2)

    
    def fitPDF(self, family):
        """ Fit a probability density function (of type <family>) """

        # TODO...
        raise NotImplementedError()
    
    
    def plot(self,fig=None,color='black',norm=False):
        """
        Plot the histogram.  

        If provided current data is added to <fig>, a matplotlib plot 
        identifier.

        <norm> indicates whether the raw counts or normalized values 
        should be plotted.
        """
        import matplotlib.pyplot as plt

        plt.ion()
            ## Interactive plots -- go.

        xs = []; ys = []
        if norm is True:
            if self.h_norm is None: 
                self.norm()
            xs,ys = zip(*sorted(self.h_norm.items()))
        else:
            xs,ys = zip(*sorted(self.h.items()))

        ax = None
        if fig is None:
            fig = plt.figure()
            ax = fig.add_subplot(111)
        else:
            ax = fig.axes[0]

        # Find the min width for bars. And plot!
        width = min(
            [xs[ii+1] - xs[ii] for ii in range(len(xs)-1)])
        ax.bar(xs,ys,
                width=width,
                alpha=0.4,
                color=color,edgecolor=color,
                align='center',
                label=self.name)
        plt.show()
        
        return fig


