# coding: utf-8
def solve(n, lows, highs):
    import numpy as np
    n_simulate = 1000000
    amount_received = [0,0,0]
    prob = 0
    for i in range(n_simulate):
        amounts = [np.random.uniform(lows[i],highs[i]) for i in range(3)]
        if sum(amounts) <= n:
            prob += 1
            for i in range(3):
                amount_received[i] += amounts[i]

        else:
            pass
    prob = prob / (n_simulate) 
    expect = [amount_received[i] / n_simulate for i in range(3)]

    probability, ex1, ex2, ex3 = round(prob,2), round(expect[0],2), round(expect[1],2), round(expect[2],2)
    return (probability, ex1, ex2, ex3)
