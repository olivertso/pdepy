"""
Este módulo contém as funções comuns para equações diferenciais parciais
em estados estacionários.
"""

import numpy as np

__all__ = ['set_u']

def set_u(xn, yn, bound_x0, bound_xf, bound_y0, bound_yf):
    """
    Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as condições
    de contorno.
    """
    u = np.empty((xn+1, yn+1))

    u[0, :]  = bound_x0
    u[-1, :] = bound_xf
    u[:, 0]  = bound_y0
    u[:, -1] = bound_yf

    return u
