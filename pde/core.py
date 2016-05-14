"""
Métodos numéricos para equações diferenciais parciais.

Classes
-------
    - Heat1D: equação do calor.
"""

__all__ = ['Heat1D']

import numpy as np

class Heat1D(object):
    """
    Equação do calor:
        u_t = u_xx

    Métodos:
        - Método explícito.
    """

    def explicit(self, xn, xf, yn, yf, cond):
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
        cond : list
            Lista de funções. 'cond[0]' é as condições iniciais,
            'cond[1]' e 'cond[2]' são as condições de contornos
            em x=0 e 'xf', respectivamente.

        Retornos
        --------
        u : ndarray
            Uma matriz de tamanho (xn+1)*(yn+1) com os resultados,
            onde cada linha representa uma posição 'x' e cada coluna
            representa uma instante de tempo 'y'.
        """

        u = self.set_u(xn, xf, yn, yf, cond)
        a = self.cal_alpha(xn, xf, yn, yf)

        for j in np.arange(yn):
            u[1:-1, j+1] = a*(u[:-2, j] + u[2:, j]) + (1 - 2*a)*u[1:-1, j]

        return u

    def set_u(self, xn, xf, yn, yf, cond):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as
        condições iniciais e de contornos.
        """
        u = np.empty((xn+1, yn+1))
        x = np.linspace(0, xf, xn+1)
        y = np.linspace(0, yf, yn+1)

        self.set_conditions(u, x, y, cond)

        return u

    def set_conditions(self, u, x, y, cond):
        """
        Aplica as condições iniciais e de contornos na matriz 'u'.
        """
        u[:, 0]  = cond[0](x)
        u[0, :]  = cond[1](y)
        u[-1, :] = cond[2](y)

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
    g1 = lambda y: 0.
    g2 = lambda y: 9.

    u = Heat1D().explicit(xn, xf, yn, yf, [f, g1, g2])

    print(u)