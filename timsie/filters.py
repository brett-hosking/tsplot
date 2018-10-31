import numpy as np
import scipy.ndimage as ndimage 

def linear(arr,filterwidth=30):
    '''
        Generate a 1D array of linear filter coefficients

        Parameters
        ----------
        arr: array_like
            input signal to be filtered 
        filtwidth : int (odd)
            width of filter (number of samples in time domain)
        Returns
        ----------
        low pass filtered signal

    '''
    olap    = int((filterwidth+1)/2)
    kernel  = np.lib.pad(np.linspace(1,3,olap), (0,olap-1),'reflect')
    kernel  = np.divide(kernel,np.sum(kernel))
    return ndimage.convolve(arr,kernel) 
    