"""Tests for the laplace module."""

import numpy as np

from .. import laplace
from .datasets import expect_laplace_ic

def test_laplace_ic():
    axis, conds = set_inputs()

    actual = laplace.solve(axis, conds, method='ic')
    expect = expect_laplace_ic

    assert np.allclose(actual, expect)

def set_inputs():
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

    return (axis, conds)
