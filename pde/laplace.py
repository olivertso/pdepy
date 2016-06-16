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

_METHODS = ['c']

def solve(domain, conds, method='c'):
    """
    Methods
    -------
        * c: central
        * TODO: u: upwind

    Parameters
    ----------
    domain : array_like
        [xn, xf, yn, yf], 'xn' and 'yn' are the number of partitions at
        axis 'x' and 'y', 'xf' and 'yf' are the final positions; [int,
        float, int, float].
    conds : array_like
        Boundary conditions; [bound_x0, bound_xf, bound_y0, bound_yf],
        each element should be a scalar or an array_like of size 'xn+1'
        for 'cond_x' and size 'yn+1' for 'cond_y'.
    method : string | optional
        Finite-difference method.

    Returns
    -------
    u : ndarray
        A matrix of size (xn+1)*(yn+1); u[x, y].
    """
    base.check_method(method, _METHODS)

    u      = steady.set_u(*domain[::2], *conds)
    consts = _cal_constants(*domain)

    _implicit(u, *domain[::2], *consts)

    return u

def _implicit(u, xn, yn, 𝛂, β):
    """Métodos de diferenças finitas implícitos."""
    mat = _set_mat(𝛂, β, xn, yn)
    vec = _set_vec(𝛂, β, u)

    x = linalg.solve(mat, vec)

    u[1:-1, 1:-1] = np.reshape(x, (xn-1, yn-1), 'F')

def _set_mat(𝛂, β, xn, yn):
    """Monta a matriz do sistema em '_implicit()'."""
    n = (xn-1) * (yn-1)

    main = np.full(n, - 2 * (𝛂 + β))
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

def _cal_constants(xn, xf, yn, yf):
    """Calcula as constantes '𝛂' e 'β'."""
    𝛂 = (xf / xn)**2
    β = (yf / yn)**2

    return (𝛂, β)
