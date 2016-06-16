"""
Este módulo contém as funções comuns dos métodos de diferenças finitas
para equações diferenciais parciais.
"""

import sys

import numpy as np

__all__ = ['set_axis', 'check_method']

def set_axis(xn, xf, yn, yf):
    """Retorna os vetores dos eixos 'x' e 'y'."""
    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    return (x, y)

def check_method(method, methods):
    """Verifica se o método numérico 'method' é válido."""
    if method not in methods:
        sys.exit('Value \'' + method + '\' for argument \'method\' is '
                 'not valid.')
