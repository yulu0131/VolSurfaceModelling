import math
from matplotlib.pyplot import *
from numpy import *
from numpy.random import standard_normal

'''

geometric brownian motion with drift!

Spezifikationen:

mu=drift factor [Annahme von Risikoneutralitaet]

sigma: volatility in %

T: time span

dt: lenght of steps

S0: Stock Price in t=0

W: Brownian Motion with Drift N[0,1]

'''

T = 1
mu = 0
sigma = 1
S0 = 20
dt = 0.01

Steps = round(T / dt)
t = (arange(0, Steps))
x = arange(0, Steps)
W = (standard_normal(size=Steps) + mu * t)
# standard brownian motion
X = (mu - 0.5 * sigma ** 2) * dt + (sigma * sqrt(dt) * W)
# geometric brownian motion
y = S0 * math.e ** X
plot(t, y)

show()
