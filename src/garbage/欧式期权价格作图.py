import math

import matplotlib.pyplot as plt
from src.option_pricer.american_option import vanilla
import numpy as np


def main():
    spot = np.linspace(1, 120, 120)
    strike = 100
    t = 0.5
    r = 0.03
    b = 0
    vol = 0.3

    s0 = spot
    call_pv = np.zeros(120)
    max_array = np.zeros(120)

    for i in range(len(spot)):
        call_pv[i] = vanilla("C", spot[i], r, b, vol, strike, t)
        max_array[i] = max(s0[i] - strike * math.exp(- r * t), 0)

    # plt.plot(spot, s0)
    plt.plot(spot, call_pv)
    # plt.plot(spot, max_array)
    plt.show()


def main1():
    spot = 80
    strike = 100
    t = np.linspace(1, 0.1, 100)
    r = 0.03
    b = 0
    vol = 0.3

    s0 = spot
    call_pv = np.zeros(100)

    for i in range(len(t)):
        call_pv[i] = vanilla("C", spot, r, b, vol, strike, t[i])

    # plt.plot(spot, s0)
    plt.plot(t, call_pv)
    # plt.plot(spot, max_array)
    plt.show()


main1()
