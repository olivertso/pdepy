"""
Finite-difference solver for wave equation:
    u_yy = u_xx.

Initial and boundary conditions:
    u(x, 0)   = init(x),     0 <= x <= xf,
    u_y(x, 0) = d_init(x),   0 <= x <= xf,
    u(0, y)   = bound_x0(y), 0 <= y <= yf,
    u(xf, y)  = bound_xf(y), 0 <= y <= yf.
"""

import numpy as np
from scipy import linalg

from . import base
from . import time

__all__ = ['solve']

_METHODS = ['e', 'i']

def solve(domain, conds, method='i'):
    """
    Methods
    -------
        * e: explicit
        * i: implicit

    Parameters
    ----------
    domain : array_like
        [xn, xf, yn, yf], 'xn' and 'yn' are the number of partitions at
        axis 'x' and 'y', 'xf' and 'yf' are the final positions; [int,
        float, int, float].
    conds : array_like
        Initial and boundary conditions; [init, bound_x0, bound_xf], each
        element should be a scalar or an array_like of size 'xn+1' for
        'cond_x' and size 'yn+1' for 'cond_y'.
    method : string | optional
        Finite-difference method.

    Returns
    -------
    u : ndarray
        A matrix of size (xn+1)*(yn+1); u[x, y].
    """
    base.check_method(method, _METHODS)

    u      = time.set_u(*domain[::2], *conds[1:])
    consts = _cal_constants(*domain)

    _set_first_row(u, *consts[1:], conds[0])

    if method == 'e':
        _explicit(u, consts[0]**(-1))
    elif method == 'i':
        _implicit(u, consts[0]**(-1))

    return u

def _explicit(u, 𝛂):
    """Métodos de diferenças finitas explícitos."""
    for j in np.arange(1, u.shape[1]-1):
        u[1:-1, j+1] = 2 * u[1:-1, j] - u[1:-1, j-1] + \
                       𝛂 * (u[2:, j] - 2 * u[1:-1, j] + u[:-2, j])

def _implicit(u, 𝛂):
    """Métodos de diferenças finitas implícitos."""
    mat = _set_mat(np.shape(u)[0]-2, 𝛂)

    for j in np.arange(1, u.shape[1]-1):
        vec = _set_vec(𝛂, u[:, j-1:j+2])

        u[1:-1, j+1] = linalg.solve(mat, vec)

def _set_mat(n, 𝛂):
    """Monta a matriz do sistema em cada iteração de '_implicit()'."""
    main  = - 2 * (np.ones(n) + 𝛂)
    upper = np.ones(n-1)
    lower = np.ones(n-1)

    return np.diag(main) + np.diag(upper, 1) + np.diag(lower, -1)

def _set_vec(𝛂, u):
    """Monta o vetor do sistema em cada iteração de '_implicit()'."""
    vec = - u[:-2, 0] - u[2:, 0] + 2 * (1 + 𝛂) * u[1:-1, 0] - \
          4 * 𝛂 * u[1:-1, 1]

    vec[0]  -= u[0, 2]
    vec[-1] -= u[-1, 2]

    return vec

def _cal_constants(xn, xf, yn, yf):
    """Calcula as constantes '𝛂', 'h' e 'k'."""
    h = xf / xn
    k = yf / yn

    𝛂 = (k**2) / (h**2)

    return (𝛂, h, k)

def _set_first_row(u, h, k, d_init):
    """
    Determina a primeira linha da malha interior. 'd_init' pode ser um
    escalar ou um vetor de tamanho do 'x'.
    """
    u[1:-1, 1] = (u[:, 0] + k * d_init)[1:-1] + k**2 / 2 * \
                 (u[2:, 0] - 2 * u[1:-1, 0] + u[:-2, 0]) / (h**2)
