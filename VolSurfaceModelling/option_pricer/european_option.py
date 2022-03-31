import math
from scipy.stats import norm
from scipy.optimize import fsolve
import numpy as np


def vanilla(option_type, s, r, b, vol, strike, t):
    d_1 = (math.log(s/strike) + (b + vol * vol * 0.5) * t) / (vol * math.sqrt(t))
    d_2 = d_1 - vol * math.sqrt(t)

    if option_type == "C":
        pv = s * math.exp((b - r) * t) * norm.cdf(d_1) - strike * math.exp(-r * t) * norm.cdf(d_2)
    else:
        pv = strike * math.exp(-r * t) * norm.cdf(-d_2) - s * math.exp((b - r) * t) * norm.cdf(-d_1)

    return pv


def find_vol(option_type, s, r, b, strike, t, pv):
    func = lambda vol: vanilla(option_type, s, r, b, vol, strike, t) - pv
    vol_init = np.array([1])
    root = fsolve(func,
                  vol_init,
                  xtol=1e-6
                  )
    return root[0]
