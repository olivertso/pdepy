"""
Este módulo contém as funções comuns para equações diferenciais parciais
em estados estacionários.
"""

import numpy as np

__all__ = ["set_u"]


def set_u(x, y, bound_x0, bound_xf, bound_y0, bound_yf):
    """Inicializa a matriz 'u' com as condições de contorno."""
    u = np.empty((x.size, y.size))

    u[0, :] = bound_x0
    u[-1, :] = bound_xf
    u[:, 0] = bound_y0
    u[:, -1] = bound_yf

    return u
