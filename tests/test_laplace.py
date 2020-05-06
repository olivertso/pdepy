import numpy as np
import pytest

from pdepy import laplace


class TestLaplace:
    @pytest.fixture
    def inputs(self):
        def initial_function(x, y):
            return (x - 1) ** 2 - (y - 2) ** 2

        xn, xf, yn, yf = 3, 3.0, 4, 4.0

        x = np.linspace(0, xf, xn + 1)
        y = np.linspace(0, yf, yn + 1)

        bound_x0 = initial_function(0, y)
        bound_xf = initial_function(xf, y)
        bound_y0 = initial_function(x, 0)
        bound_yf = initial_function(x, yf)

        axis = x, y
        conds = bound_x0, bound_xf, bound_y0, bound_yf

        return axis, conds

    def test_ic(self, inputs):
        axis, conds = inputs

        actual = laplace.solve(axis, conds, method="ic")
        expect = [
            [-3.0, 0.0, 1.0, 0.0, -3.0],
            [-4.0, -1.0, -0.0, -1.0, -4.0],
            [-3.0, -0.0, 1.0, -0.0, -3.0],
            [0.0, 3.0, 4.0, 3.0, 0.0],
        ]

        assert np.allclose(actual, expect)
