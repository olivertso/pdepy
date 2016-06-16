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
    method = 'c'

    u = laplace.solve(domain, conds, method=method)

    print(u)

def test_parabolic():
    xn = 4
    xf = 4.
    yn = 2
    yf = 1.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    p = np.ones((xn-1, yn))
    q = (lambda x: x - np.ones((xn-1, yn))*2.)(x[1:-1, np.newaxis])
    r = np.ones((xn-1, yn)) * (-3)
    s = np.zeros((xn-1, yn))

    init   = (lambda x: x**2 - 4*x + 5)(x)
    bound1 = (lambda y: 5 * np.exp(-y))(y)
    bound2 = (lambda y: 5 * np.exp(-y))(y)

    domain = (xn, xf, yn, yf)
    params = (p, q, r, s)
    conds  = (init, bound1, bound2)
    method = 'iu'

    u = parabolic.solve(domain, params, conds, method=method)

    print(u)

def test_wave():
    xn = 4
    xf = 1.
    yn = 4
    yf = 0.5

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    d_init = 1
    init   = (lambda x: x * (1 - x))(x)
    bound1 = (lambda y: y * (1 - y))(y)
    bound2 = (lambda y: y * (1 - y))(y)

    domain = (xn, xf, yn, yf)
    conds  = (d_init, init, bound1, bound2)
    method = 'i'

    u = wave.solve(domain, conds, method=method)

    print(u)

test_laplace()
print()
test_parabolic()
print()
test_wave()
