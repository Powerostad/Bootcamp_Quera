# coding: utf-8
def solve(arr):
    import numpy as np
    import scipy as sp
    import math
    total_n = sum(len(array) for array in arr)
    n_arr = len(arr)
    total_mean = np.mean(np.concatenate(arr))

    ssb = sum(len(i) * (np.mean(i) - total_mean) ** 2 for i in arr)
    ssw = sum((len(i) - 1) * np.var(i,ddof=1) for i in arr)
    df_b = n_arr - 1
    df_w = total_n - n_arr
    
    msb = ssb / df_b
    msw = ssw / df_w

    f_statistic = msb / msw

    
    p_value = 1 - sp.stats.f.cdf(f_statistic, df_b, df_w)

    
    confidence = (1 - p_value ) * 100

    return round(confidence,2)
