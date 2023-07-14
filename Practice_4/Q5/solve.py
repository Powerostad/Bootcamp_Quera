# coding: utf-8
def solve(mu, arr):
    import numpy as np
    import scipy as sp
    import math

    array = np.array(arr)
    t,p = sp.stats.ttest_1samp(array,popmean=mu)

    max_p = (1-p)*100
    return round(max_p,3)
