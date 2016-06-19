"""
TODO:

[[-3.,  0.,  1.,  0., -3.],
 [-4., -1., -0., -1., -4.],
 [-3., -0.,  1., -0., -3.],
 [ 0.,  3.,  4.,  3.,  0.]]
"""

import numpy as np

from pde import laplace
from pde import parabolic
from pde import wave

def test_laplace():
    xn = 3
    xf = 3.
    yn = 4
    yf = 4.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    f = lambda x, y: (x - 1)**2 - (y - 2)**2
    bound_x0 = f(0, y)
    bound_xf = f(xf, y)
    bound_y0 = f(x, 0)
    bound_yf = f(x, yf)

    domain = (xn, xf, yn, yf)
    conds  = (bound_x0, bound_xf, bound_y0, bound_yf)

    print(laplace.solve(domain, conds, method='ic'))

def test_parabolic():
    xn = 4
    xf = 4.
    yn = 5
    yf = 0.5

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    init   = (lambda x: x**2 - 4*x + 5)(x)
    bound1 = (lambda y: 5 * np.exp(-y))(y)
    bound2 = (lambda y: 5 * np.exp(-y))(y)

    p = 1
    q = 1
    r = -3
    s = 3

    domain = (xn, xf, yn, yf)
    conds  = (init, bound1, bound2)
    params = (p, q, r, s)

    print(parabolic.solve(domain, params, conds, method='ec'))
    print()
    print(parabolic.solve(domain, params, conds, method='eu'))
    print()
    print(parabolic.solve(domain, params, conds, method='ic'))
    print()
    print(parabolic.solve(domain, params, conds, method='iu'))

def test_wave():
    xn = 4
    xf = 1.
    yn = 4
    yf = 1.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    d_init = 1
    init   = (lambda x: x * (1 - x))(x)
    bound1 = (lambda y: y * (1 - y))(y)
    bound2 = (lambda y: y * (1 - y))(y)

    domain = (xn, xf, yn, yf)
    conds  = (d_init, init, bound1, bound2)

    print(wave.solve(domain, conds, method='e'))
    print()
    print(wave.solve(domain, conds, method='i'))

test_laplace()
# print()
# test_parabolic()
# print()
# test_wave()
