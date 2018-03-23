"""Tests for the laplace module."""

import numpy as np

from pde import laplace

expect_laplace_ic = [
    [-3.,  0.,  1.,  0., -3.],
    [-4., -1., -0., -1., -4.],
    [-3., -0.,  1., -0., -3.],
    [0.,  3.,  4.,  3.,  0.]
]


def test_laplace_ic():
    axis, conds = set_inputs()

    actual = laplace.solve(axis, conds, method='ic')
    expect = expect_laplace_ic

    assert np.allclose(actual, expect)


def set_inputs():
    xn, xf, yn, yf = 3, 3., 4, 4.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    bound_x0 = initial_function(0, y)
    bound_xf = initial_function(xf, y)
    bound_y0 = initial_function(x, 0)
    bound_yf = initial_function(x, yf)

    axis = (x, y)
    conds = (bound_x0, bound_xf, bound_y0, bound_yf)

    return (axis, conds)


def initial_function(x, y):
    return (x-1)**2 - (y-2)**2
