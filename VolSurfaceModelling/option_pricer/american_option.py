import numpy as np
import math
from scipy.stats import norm
from scipy.stats import mvn
from option_pricer.european_option import vanilla
from scipy.optimize import fsolve


def american_option(option_type, spot, r, b, vol, t, strike):
    if option_type == "C":
        return bjerksund_stensland_2002_call(spot, strike, t, r, b, vol)
    else:
        put__x = spot
        put_fs = strike
        put_b = -b
        put_r = r - b

        return bjerksund_stensland_2002_call(put_fs, put__x, t, put_r, put_b, vol)


def find_vol(option_type, spot, r, b, t, strike, pv):
    vol_init = np.array([1])
    root = fsolve(find_vol_func,
                  vol_init,
                  args=(option_type, spot, r, b, t, strike, pv),
                  xtol=1e-6,
                  )
    return root[0]


def find_vol_func(vol, option_type, spot, r, b, t, strike, pv):
    return american_option(option_type, spot, r, b, vol, t, strike) - pv


def bjerksund_stensland_2002_call(fs, x, t, r, b, v):
    european_pv = vanilla('C', fs, r, b, v, x, t)

    if b >= r:
        return european_pv

    v2 = v ** 2
    t1 = 0.5 * (math.sqrt(5) - 1) * t
    t2 = t

    beta_inside = ((b / v2 - 0.5) ** 2) + 2 * r / v2
    beta_inside = abs(beta_inside)
    beta = (0.5 - b / v2) + math.sqrt(beta_inside)
    b_infinity = (beta / (beta - 1)) * x
    b_zero = max(x, (r / (r - b)) * x)

    h1 = -(b * t1 + 2 * v * math.sqrt(t1)) * ((x * x) / ((b_infinity - b_zero) * b_zero))
    h2 = -(b * t2 + 2 * v * math.sqrt(t2)) * ((x * x) / ((b_infinity - b_zero) * b_zero))

    i1 = b_zero + (b_infinity - b_zero) * (1 - math.exp(h1))
    i2 = b_zero + (b_infinity - b_zero) * (1 - math.exp(h2))

    alpha1 = (i1 - x) * (np.power(i1, -beta))
    alpha2 = (i2 - x) * (np.power(i2, -beta))

    if fs >= i2:
        return fs - x
    else:
        return (alpha2 * (fs ** beta)
                - alpha2 * phi(fs, t1, beta, i2, i2, r, b, v)
                + phi(fs, t1, 1, i2, i2, r, b, v)
                - phi(fs, t1, 1, i1, i2, r, b, v)
                - x * phi(fs, t1, 0, i2, i2, r, b, v)
                + x * phi(fs, t1, 0, i1, i2, r, b, v)
                + alpha1 * phi(fs, t1, beta, i1, i2, r, b, v)
                - alpha1 * psi(fs, t2, beta, i1, i2, i1, t1, r, b, v)
                + psi(fs, t2, 1, i1, i2, i1, t1, r, b, v)
                - psi(fs, t2, 1, x, i2, i1, t1, r, b, v)
                - x * psi(fs, t2, 0, i1, i2, i1, t1, r, b, v)
                + x * psi(fs, t2, 0, x, i2, i1, t1, r, b, v))


def psi(fs, t2, gamma, h, i2, i1, t1, r, b, v):
    vsqrt_t1 = v * math.sqrt(t1)
    vsqrt_t2 = v * math.sqrt(t2)

    bgamma_t1 = (b + (gamma - 0.5) * (v ** 2)) * t1
    bgamma_t2 = (b + (gamma - 0.5) * (v ** 2)) * t2

    d1 = (math.log(fs / i1) + bgamma_t1) / vsqrt_t1
    d3 = (math.log(fs / i1) - bgamma_t1) / vsqrt_t1

    d2 = (math.log((i2 ** 2) / (fs * i1)) + bgamma_t1) / vsqrt_t1
    d4 = (math.log((i2 ** 2) / (fs * i1)) - bgamma_t1) / vsqrt_t1

    e1 = (math.log(fs / h) + bgamma_t2) / vsqrt_t2
    e2 = (math.log((i2 ** 2) / (fs * h)) + bgamma_t2) / vsqrt_t2
    e3 = (math.log((i1 ** 2) / (fs * h)) + bgamma_t2) / vsqrt_t2
    e4 = (math.log((fs * (i1 ** 2)) / (h * (i2 ** 2))) + bgamma_t2) / vsqrt_t2

    tau = math.sqrt(t1 / t2)
    lambda1 = (-r + gamma * b + 0.5 * gamma * (gamma - 1) * (v ** 2))
    kappa = (2 * b) / (v ** 2) + (2 * gamma - 1)

    psi = math.exp(lambda1 * t2) * (fs ** gamma) * (cbnd(-d1, -e1, tau)
                                                    - ((i2 / fs) ** kappa) * cbnd(-d2, -e2, tau)
                                                    - ((i1 / fs) ** kappa) * cbnd(-d3, -e3, -tau)
                                                    + ((i1 / i2) ** kappa) * cbnd(-d4, -e4, -tau))
    return psi


def phi(fs, t, gamma, h, i, r, b, v):
    d1 = -(math.log(fs / h) + (b + (gamma - 0.5) * (v ** 2)) * t) / (v * math.sqrt(t))
    d2 = d1 - 2 * math.log(i / fs) / (v * math.sqrt(t))

    lambda1 = (-r + gamma * b + 0.5 * gamma * (gamma - 1) * (v ** 2))
    kappa = (2 * b) / (v ** 2) + (2 * gamma - 1)

    phi = math.exp(lambda1 * t) * (fs ** gamma) * (norm.cdf(d1) - ((i / fs) ** kappa) * norm.cdf(d2))

    return phi


def cbnd(a, b, rho):
    lower = np.array([0, 0])
    upper = np.array([a, b])
    infin = np.array([0, 0])
    correl = rho
    error, value, inform = mvn.mvndst(lower, upper, infin, correl)
    return value
