"""
Este módulo contém as funções comuns para equações diferenciais parciais
dependente de uma variável temporal.
"""

import numpy as np

__all__ = ['set_u']

def set_u(xn, yn, init, bound_x0, bound_xf):
    """
    Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as condições
    iniciais e de contorno.
    """
    u = np.empty((xn+1, yn+1))

    u[:, 0]  = init
    u[0, :]  = bound_x0
    u[-1, :] = bound_xf

    return u
