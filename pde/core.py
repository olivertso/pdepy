"""
Métodos numéricos para equações diferenciais parciais.

Classes
-------
    - Heat1D: equação do calor.
"""

__all__ = ['Heat1D']

import types
import numpy as np

class Heat1D(object):
    """
    Equação do calor:
        u_t = u_xx

    Métodos:
        - Método explícito.
    """

    def explicit(self, xn, xf, yn, yf, conds):
        """
        Método explícito.

        Propriedade de max-min:
            a <= 1/2
            ou
            k <= (h**2)/2

        Parâmetros
        ----------
        xn : int
            Número de pontos no eixo x menos um.
        xf : float
            Posição final no eixo x.
        yn : int
            Número de pontos no eixo y menos um.
        yf : float
            Posição final no eixo y.
        conds : list
            'conds[0]' é as condições iniciais, 'conds[1]' e 'conds[2]'
            são as condições de contornos em x=0 e 'xf', respectivamente.
            Cada elemento de 'conds' pode ser do tipo funciont, scalar ou
            array_like.

        Retornos
        --------
        u : ndarray
            Uma matriz de tamanho (xn+1)*(yn+1) com os resultados,
            onde cada linha representa uma posição 'x' e cada coluna
            representa uma instante de tempo 'y'.
        """

        u = self.set_u(xn, xf, yn, yf, conds)
        a = self.cal_alpha(xn, xf, yn, yf)

        for j in np.arange(yn):
            u[1:-1, j+1] = a*(u[:-2, j] + u[2:, j]) + (1 - 2*a)*u[1:-1, j]

        return u

    def set_u(self, xn, xf, yn, yf, conds):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as
        condições iniciais e de contornos.
        """
        u = np.empty((xn+1, yn+1))
        x = np.linspace(0, xf, xn+1)
        y = np.linspace(0, yf, yn+1)

        self.set_conditions(u, x, y, conds)

        return u

    def set_conditions(self, u, x, y, conds):
        """
        Aplica as condições iniciais e de contornos na matriz 'u'.
        """
        self.check_conds_type(conds, x, y)

        u[:, 0]  = conds[0]
        u[0, :]  = conds[1]
        u[-1, :] = conds[2]

    def check_conds_type(self, conds, x, y):
        """
        Verifica os tipos das condições iniciais e de contornos. Se
        for do tipo function, aplica os valores de 'x' ou 'y'.
        """
        if type(conds[0]) == types.FunctionType:
            conds[0] = conds[0](x)

        if type(conds[1]) == types.FunctionType:
            conds[1] = conds[1](y)

        if type(conds[2]) == types.FunctionType:
            conds[2] = conds[2](y)

    def cal_alpha(self, xn, xf, yn, yf):
        """Calcula a constante alpha 'a'."""
        h = xf / xn
        k = yf / yn

        return k / h**2

if __name__ == '__main__':
    xn = 3
    xf = 3.
    yn = 6
    yf = 3.

    f  = lambda x: x**2
    g1 = np.zeros(yn+1)
    g2 = 9.

    u = Heat1D().explicit(xn, xf, yn, yf, [f, g1, g2])

    print(u)