import numpy as np

from pde import laplace

def _test_laplace():
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

_test_laplace()
