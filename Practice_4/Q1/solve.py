# coding: utf-8
def solve(arr):
    import numpy as np
    mu_list = []
    for i in arr:
        mu_list.append(i/20)
    mu_array = np.array(mu_list)
    return mu_array.mean()
