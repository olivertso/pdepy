"""Tests for the parabolic module."""

import numpy as np

from .. import parabolic
from .datasets import expect_parabolic

def test_parabolic_ec():
    axis, conds, params = set_inputs()

    actual = parabolic.solve(axis, params, conds, method='ec')
    expect = expect_parabolic['ec']

    assert np.allclose(actual, expect)

def test_parabolic_eu():
    axis, conds, params = set_inputs()

    actual = parabolic.solve(axis, params, conds, method='eu')
    expect = expect_parabolic['eu']

    assert np.allclose(actual, expect)

def test_parabolic_ic():
    axis, conds, params = set_inputs()

    actual = parabolic.solve(axis, params, conds, method='ic')
    expect = expect_parabolic['ic']

    assert np.allclose(actual, expect)

def test_parabolic_iu():
    axis, conds, params = set_inputs()

    actual = parabolic.solve(axis, params, conds, method='iu')
    expect = expect_parabolic['iu']

    assert np.allclose(actual, expect)

def set_inputs():
    xn, xf, yn, yf = 4, 4., 5, 0.5

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    init  = x**2 - 4*x + 5
    bound = 5 * np.exp(-y)

    p, q, r, s = 1, 1, -3, 3

    axis   = (x, y)
    conds  = (init, bound, bound)
    params = (p, q, r, s)

    return (axis, conds, params)
