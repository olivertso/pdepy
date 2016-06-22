"""TODO"""

import numpy as np

from pde import laplace
from pde import parabolic
from pde import wave

def test_laplace():
    xn, xf, yn, yf = 3, 3., 4, 4.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    f = lambda x, y: (x-1)**2 - (y-2)**2
    bound_x0 = f(0, y)
    bound_xf = f(xf, y)
    bound_y0 = f(x, 0)
    bound_yf = f(x, yf)

    axis  = (x, y)
    conds = (bound_x0, bound_xf, bound_y0, bound_yf)

    print(laplace.solve(axis, conds, method='ic'))

def test_parabolic():
    xn, xf, yn, yf = 4, 4., 5, 0.5

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    init  = x**2 - 4*x + 5
    bound = 5 * np.exp(-y)

    p, q, r, s = 1, 1, -3, 3

    axis   = (x, y)
    conds  = (init, bound, bound)
    params = (p, q, r, s)

    print(parabolic.solve(axis, params, conds, method='ec'))
    print()
    print(parabolic.solve(axis, params, conds, method='eu'))
    print()
    print(parabolic.solve(axis, params, conds, method='ic'))
    print()
    print(parabolic.solve(axis, params, conds, method='iu'))

def test_wave():
    xn, xf, yn, yf = 4, 1., 4, 1.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    d_init = 1
    init   = x * (1-x)
    bound  = y * (1-y)

    axis  = (x, y)
    conds = (d_init, init, bound, bound)

    print(wave.solve(axis, conds, method='e'))
    print()
    print(wave.solve(axis, conds, method='i'))

test_laplace()
print()
test_parabolic()
print()
test_wave()
