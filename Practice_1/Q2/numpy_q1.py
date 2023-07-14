import numpy as np

def replace_odd(array):
    array[array % 2 == 1] = -1
    output = array
    return output

