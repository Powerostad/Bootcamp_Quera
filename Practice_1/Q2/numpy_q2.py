import numpy as np
def p2p_distance(array):
    n = array.shape[0]
    distances = np.zeros((n, n))
    distances += np.sum((array[:, np.newaxis, :] - array[np.newaxis, :, :]) ** 2, axis=-1)
    output = np.sqrt(distances)
    return output