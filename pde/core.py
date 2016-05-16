"""
Métodos de diferenças finitas para equações diferenciais parciais.

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
        u_t = P(x, y)*u_xx + S(x, y)

    Métodos:
        - Diferenças finitas centrais explícito

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
        Cada elemento de 'conds' pode ser uma função vetorial de uma
        variável, ou um escalar, ou um vetor de tamanhoxn+1' ou
        'yn+1'.
    P, S : function, scalar, array_like | optional
        É uma função vetorial de duas variáveis, ou um escalar, ou
        uma matriz de tamanho (xn-1)*yn.

    Retornos
    --------
    u : ndarray
        Uma matriz de tamanho (xn+1)*(yn+1) com os resultados,
        onde cada linha representa uma posição 'x' e cada coluna
        representa uma instante de tempo 'y'.
    """

    def exp_central(self, xn, xf, yn, yf, conds, P=1, S=0):
        """
        Diferenças finitas centrais explícito.

        Propriedade de max-min:
            a <= 1/2
            ou
            k <= (h**2)/2
        """
        x, y = self.set_axis(xn, xf, yn, yf)

        u    = self.set_u(x, y, conds)
        a, k = self.cal_alpha(xn, xf, yn, yf)
        P    = self.func_to_val(P, x, y)
        S    = self.func_to_val(S, x, y)

        for j in np.arange(yn):
            u[1:-1, j+1] = a * P[:, j] * (u[:-2, j] + u[2:, j]) + \
                           (1 - 2 * a * P[:, j]) * u[1:-1, j] + \
                           k * S[:, j]

        return u

    def set_axis(self, xn, xf, yn, yf):
        """Retorna os vetores dos eixos 'x' e 'y'."""
        x = np.linspace(0, xf, xn+1)
        y = np.linspace(0, yf, yn+1)

        return x, y

    def set_u(self, x, y, conds):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as
        condições iniciais e de contornos.
        """
        u = np.empty((len(x), len(y)))
        self.set_conditions(u, x, y, conds)

        return u

    def cal_alpha(self, xn, xf, yn, yf):
        """Calcula a constante alpha 'a'."""
        h = xf / xn
        k = yf / yn

        return k / h**2, k

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
        conds[0] = self.func_to_val(conds[0], x)
        conds[1] = self.func_to_val(conds[1], y)
        conds[2] = self.func_to_val(conds[2], y)

    def func_to_val(self, func_or_val, *args):
        """
        Se 'func_or_val' for uma função, aplica os valores de 'args',
        se for um escalar, retorna uma matriz com valores desse escalar,
        se for um vetor ou uma matriz, retorna sem modificar.
        """
        if isinstance(func_or_val, types.FunctionType):
            if len(args) == 2:
                args = np.meshgrid(args[1], args[0])
            return func_or_val(*args[::-1])

        elif isinstance(func_or_val, (int, float)):
            if len(args) == 1:
                return func_or_val
            elif len(args) == 2:
                x = np.ones((len(args[0])-2, len(args[1])-1))
                return func_or_val * x

        else:
            return func_or_val

if __name__ == '__main__':
    xn = 3
    xf = 3.
    yn = 6
    yf = 3.

    f  = lambda x: x**2
    g1 = np.zeros(yn+1)
    g2 = 9.
    conds = [f, g1, g2]

    u = Heat1D().exp_central(xn, xf, yn, yf, conds)

    print(u)