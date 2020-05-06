import numpy as np
import pytest

from pdepy import wave


class TestWave:
    @pytest.fixture
    def inputs(self):
        xn, xf, yn, yf = 4, 1.0, 4, 1.0

        x = np.linspace(0, xf, xn + 1)
        y = np.linspace(0, yf, yn + 1)

        d_init = 1
        init = x * (1 - x)
        bound = y * (1 - y)

        axis = x, y
        conds = d_init, init, bound, bound

        return axis, conds

    @pytest.mark.parametrize("method", ["e", "i"])
    def test(self, inputs, method):
        axis, conds = inputs

        actual = wave.solve(axis, conds, method=method)
        expect = [
            [0.0, 0.1875, 0.25, 0.1875, 0.0],
            [0.1875, 0.375, 0.4375, 0.375, 0.1875],
            [0.25, 0.4375, 0.5, 0.4375, 0.25],
            [0.1875, 0.375, 0.4375, 0.375, 0.1875],
            [0.0, 0.1875, 0.25, 0.1875, 0.0],
        ]

        assert np.allclose(actual, expect)
