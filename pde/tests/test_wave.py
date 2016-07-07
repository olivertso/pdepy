"""Tests for the wave module."""

import numpy as np

from .. import wave
from .datasets import expect_wave_e_i

def test_wave_e():
    axis, conds = set_inputs()

    actual = wave.solve(axis, conds, method='e')
    expect = expect_wave_e_i

    assert np.allclose(actual, expect)

def test_wave_i():
    axis, conds = set_inputs()

    actual = wave.solve(axis, conds, method='i')
    expect = expect_wave_e_i

    assert np.allclose(actual, expect)

def set_inputs():
    xn, xf, yn, yf = 4, 1., 4, 1.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    d_init = 1
    init   = x * (1-x)
    bound  = y * (1-y)

    axis  = (x, y)
    conds = (d_init, init, bound, bound)

    return (axis, conds)
