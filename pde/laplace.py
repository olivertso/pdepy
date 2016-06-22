"""
Finite-difference solver for Laplace equation:
    u_xx + u_yy = 0.

Boundary conditions:
    u(x, y) = bound(x, y).
"""

import numpy as np
from scipy import linalg

from . import base
from . import steady

__all__ = ['solve']

_METHODS = ['ic']

def solve(axis, conds, method='ic'):
    """
    Methods
    -------
        * ic: implicit central

    Parameters
    ----------
    axis : array_like
        Axis 'x' and 'y'; [x, y], each element should be an array_like.
    conds : array_like
        Boundary conditions; [bound_x0, bound_xf, bound_y0, bound_yf],
        each element should be a scalar or an array_like of size of 'x'
        for 'cond_y's and size of 'y' for 'cond_x's.
    method : string | optional
        Finite-difference method.

    Returns
    -------
    u : ndarray
        A 2-D ndarray; u[x, y].
    """
    base.check_method(method, _METHODS)

    u = steady.set_u(*axis, *conds)
    consts = _cal_constants(*axis)

    _implicit(u, *axis, *consts)

    return u

def _implicit(u, x, y, 𝛂, β):
    """Métodos de diferenças finitas implícitos."""
    xn, yn = x.size, y.size

    mat = _set_mat(𝛂, β, xn-1, yn-1)
    vec = _set_vec(𝛂, β, u)

    x = linalg.solve(mat, vec)

    u[1:-1, 1:-1] = np.reshape(x, (xn-2, yn-2), 'F')

def _set_mat(𝛂, β, xn, yn):
    """Monta a matriz do sistema em '_implicit()'."""
    n = (xn-1) * (yn-1)

    main = np.full(n, -2*(𝛂+β))
    sub1 = np.full(n-1, β)
    sub2 = np.full(n-xn+1, 𝛂)

    sub1[xn-2:-1:xn-1] = 0

    return np.diag(main) + np.diag(sub1, 1) + np.diag(sub1, -1) + \
           np.diag(sub2, xn-1) + np.diag(sub2, -xn+1)

def _set_vec(𝛂, β, u):
    """Monta o vetor do sistema em '_implicit()'."""
    vec = np.zeros_like((u[1:-1, 1:-1]))

    vec[0, :]  -= β * u[0, 1:-1]
    vec[-1, :] -= β * u[-1, 1:-1]
    vec[:, 0]  -= 𝛂 * u[1:-1, 0]
    vec[:, -1] -= 𝛂 * u[1:-1, -1]

    return np.reshape(vec, np.size(vec), 'F')

def _cal_constants(x, y):
    """Calcula as constantes '𝛂' e 'β'."""
    𝛂 = (x[-1] / (x.size-1)) ** 2
    β = (y[-1] / (y.size-1)) ** 2

    return (𝛂, β)
