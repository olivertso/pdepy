"""
Finite-difference solver for parabolic equation:
    u_y = p(x, y)*u_xx + q(x, y)*u_x + r(x, y)*u + s(x, y).

Initial and boundary conditions:
    u(x, 0)  = init(x),     0 <= x <= xf,
    u(0, y)  = bound_x0(y), 0 <= y <= yf,
    u(xf, y) = bound_xf(y), 0 <= y <= yf.
"""

import numpy as np
from scipy import linalg

from . import base
from . import time

__all__ = ['solve']

_METHODS = ['ec', 'eu', 'ic', 'iu']

def solve(domain, params, conds, method='iu'):
    """
    Methods
    -------
        * ec: explicit central
        * eu: explicit upwind
        * ic: implicit central
        * iu: implicit upwind

    Parameters
    ----------
    domain : array_like
        [xn, xf, yn, yf], 'xn' and 'yn' are the number of partitions at
        axis 'x' and 'y', 'xf' and 'yf' are the final positions; [int,
        float, int, float].
    params : array_like
        The parameters of the equation; [p, q, r, s], each element should
        be a scalar or a matrix of size '(xn-1)*yn'.
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

    u      = time.set_u(*domain[::2], *conds)
    consts = _cal_constants(*domain)

    𝛉 = _set_𝛉(method)

    if method[0] == 'e':
        _explicit(u, 𝛉, *consts, *params)
    elif method[0] == 'i':
        _implicit(u, 𝛉, *consts, *params)

    return u

def _explicit(u, 𝛉, 𝛂, β, k, p, q, r, s):
    """Métodos de diferenças finitas explícitos."""
    for j in np.arange(u.shape[1]-1):
        u[1:-1, j+1] = (𝛂 * p[:, j] + \
                       β * (𝛉 * np.abs(q[:, j]) - q[:, j])) * \
                       u[:-2, j] + \
                       (𝛂 * p[:, j] + \
                       β * (𝛉 * np.abs(q[:, j]) + q[:, j])) * \
                       u[2:, j] + \
                       (1 + k * r[:, j] - \
                       2 * (𝛂 * p[:, j] + 𝛉 * β * np.abs(q[:, j]))) * \
                       u[1:-1, j] + \
                       k * s[:, j]

def _implicit(u, 𝛉, 𝛂, β, k, p, q, r, s):
    """Métodos de diferenças finitas implícitos."""
    for j in np.arange(u.shape[1]-1):
        params1 = (p[:, j], q[:, j], r[:, j])
        params2 = (p[:, j], q[:, j], s[:, j])

        mat = _set_mat(𝛉, 𝛂, β, k, *params1)
        vec = _set_vec(𝛉, 𝛂, β, k, *params2, u[:, j:j+2])

        u[1:-1, j+1] = linalg.solve(mat, vec)

def _set_mat(𝛉, 𝛂, β, k, p, q, r):
    """Monta a matriz do sistema em cada iteração de '_implicit()'."""
    main  = - 1 + k * r[:] - 2 * (𝛂 * p[:] + 𝛉 * β * np.abs(q[:]))
    upper = 𝛂 * p[:-1] + β * (𝛉 * np.abs(q[:-1]) + q[:-1])
    lower = 𝛂 * p[1:]  + β * (𝛉 * np.abs(q[1:])  - q[1:] )

    return np.diag(main) + np.diag(upper, 1) + np.diag(lower, -1)

def _set_vec(𝛉, 𝛂, β, k, p, q, s, u):
    """Monta o vetor do sistema em cada iteração de '_implicit()'."""
    vec      = - u[1:-1, 0] - k * s[:]
    vec[0]  -= (𝛂 * p[0]  + β * (𝛉 * np.abs(q[0])  - q[0] )) * u[0, 1]
    vec[-1] -= (𝛂 * p[-1] + β * (𝛉 * np.abs(q[-1]) + q[-1])) * u[-1, 1]

    return vec

def _cal_constants(xn, xf, yn, yf):
    """Calcula as constantes '𝛂', 'β' e 'k'."""
    h = xf / xn
    k = yf / yn

    𝛂 = k / h**2
    β = k / (2*h)

    return (𝛂, β, k)

def _set_𝛉(method):
    """Retorna o valor de '𝛉' conforme 'method'."""
    if method[1] =='c':
        return 0
    elif method[1] == 'u':
        return 1
