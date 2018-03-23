"""Tests for the parabolic module."""

import numpy as np

from pde import parabolic

expect_parabolic_ec = [
    [5., 4.52418709, 4.09365377, 3.7040911, 3.35160023, 3.0326533],
    [2., 1.7, 1.55620935, 1.47778737, 1.42526394, 1.38240388],
    [1., 1.2, 1.3, 1.34110468, 1.34794602, 1.3353887],
    [2., 2.1, 2.08862806, 2.0233621, 1.93434995, 1.83731231],
    [5., 4.52418709, 4.09365377, 3.7040911, 3.35160023, 3.0326533]
]

expect_parabolic_eu = [
    [5., 4.52418709, 4.09365377, 3.7040911, 3.35160023, 3.0326533],
    [2., 1.8, 1.73241871, 1.69033286, 1.64498413, 1.59228371],
    [1., 1.3, 1.44, 1.49220935, 1.49565017, 1.47265957],
    [2., 2.2, 2.21483742, 2.14866572, 2.04950544, 1.93968724],
    [5., 4.52418709, 4.09365377, 3.7040911, 3.35160023, 3.0326533]
]

expect_parabolic_ic = [
    [5., 4.52418709, 4.09365377, 3.7040911, 3.35160023, 3.0326533],
    [2., 1.79703016, 1.6552385, 1.5520893, 1.47351446, 1.41079567],
    [1., 1.1289059, 1.20763268, 1.25127267, 1.27068247, 1.27364255],
    [2., 2.02338224, 1.99854129, 1.94447906, 1.87383548, 1.79494373],
    [5., 4.52418709, 4.09365377, 3.7040911, 3.35160023, 3.0326533]
]

expect_parabolic_iu = [
    [5., 4.52418709, 4.09365377, 3.7040911, 3.35160023, 3.0326533],
    [2., 1.86888319, 1.77407366, 1.69796746, 1.63144259, 1.57006533],
    [1., 1.18897197, 1.30134642, 1.36132585, 1.38590329, 1.38698308],
    [2., 2.07733413, 2.07887471, 2.03489094, 1.96487582, 1.8813155],
    [5., 4.52418709, 4.09365377, 3.7040911, 3.35160023, 3.0326533]
]

expect_parabolic = {
    'ec': expect_parabolic_ec,
    'eu': expect_parabolic_eu,
    'ic': expect_parabolic_ic,
    'iu': expect_parabolic_iu
}


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

    init = x**2 - 4*x + 5
    bound = 5 * np.exp(-y)

    p, q, r, s = 1, 1, -3, 3

    axis = (x, y)
    conds = (init, bound, bound)
    params = (p, q, r, s)

    return (axis, conds, params)
