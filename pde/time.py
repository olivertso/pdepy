"""
Este módulo contém as funções comuns para equações diferenciais parciais
dependente de uma variável temporal.
"""

import numpy as np

__all__ = ['set_u']

def set_u(x, y, init, bound_x0, bound_xf):
    """Inicializa a matriz 'u' com as condições iniciais e de contorno."""
    u = np.empty((x.size, y.size))

    u[:, 0]  = init
    u[0, :]  = bound_x0
    u[-1, :] = bound_xf

    return u
