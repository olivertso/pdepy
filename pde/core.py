"""
Métodos de diferenças finitas para equações diferenciais parciais de
segunda ordem.

Classes
-------
    - LinParabolic: equação parabólica linear.
"""

__all__ = ['LinParabolic']

import types
import numpy as np

class LinParabolic(object):
    """
    Equação parabólica linear:
        u_t = P(x, y)*u_xx + Q(x, y)*u_x + R(x, y)*u + S(x, y),

        u(x, 0)  = conds[0](x), 0 <= x <= xf,
        u(0, y)  = conds[1](y), 0 <= y <= yf,
        u(xf, y) = conds[2](y), 0 <= y <= yf.

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
    P, Q, R, S : function, scalar, array_like | optional
        É uma função vetorial de duas variáveis, ou um escalar, ou
        uma matriz de tamanho (xn-1)*yn.
    mthd : string
        Método para resolver a equação. 'ec' para diferenças finitas
        centrais explícito.

    Retornos
    --------
    u : ndarray
        Uma matriz de tamanho (xn+1)*(yn+1) com os resultados,
        onde cada linha representa uma posição 'x' e cada coluna
        representa uma instante de tempo 'y'.
    """

    def solve(self, xn, xf, yn, yf, conds, P=1, Q=1, R=1, S=0, mthd='ec'):
        """
        Método principal. Inicializa os parâmetros e chama o método
        especificado para resolver a equação.
        """
        x, y       = self.set_axis(xn, xf, yn, yf)
        u          = self.set_u(x, y, conds)
        𝛂, β, k    = self.cal_constants(xn, xf, yn, yf)
        P, Q, R, S = self.cal_parameters(P, Q, R, S, x, y)

        if mthd == 'ec':
            self.ec(u, 𝛂, β, k, P, Q, R, S)
        else:
            u = 0

        return u

    def ec(self, u, 𝛂, β, k, P, Q, R, S):
        """
        Diferenças finitas centrais explícito.
        """
        for j in np.arange(yn):
            u[1:-1, j+1] = (𝛂 * P[:, j] - β * Q[:, j]) * u[:-2, j] + \
                           (𝛂 * P[:, j] + β * Q[:, j]) * u[2:, j] + \
                           (1 + k * R[:, j] - 2 * 𝛂 * P[:, j]) * u[1:-1, j] + \
                           k * S[:, j]

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

    def cal_constants(self, xn, xf, yn, yf):
        """Calcula as constantes '𝛂', 'β' e 'k'."""
        h = xf / xn
        k = yf / yn

        𝛂 = k / h**2
        β = k / (2 * h)

        return 𝛂, β, k

    def cal_parameters(self, P, Q, R, S, x, y):
        P = self.func_to_val(P, x, y)
        Q = self.func_to_val(Q, x, y)
        R = self.func_to_val(R, x, y)
        S = self.func_to_val(S, x, y)

        return P, Q, R, S

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
                args = np.meshgrid(args[1][1:], args[0][1:-1])
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
    xn = 4
    xf = 4.
    yn = 10
    yf = 1.

    f  = lambda x: x**2 - 4*x + 5
    g1 = lambda y: 5 * np.exp(-y)
    g2 = lambda y: 5 * np.exp(-y)
    conds = [f, g1, g2]

    Q = lambda x, y: x - 2.
    R = -3.

    u = LinParabolic().solve(xn, xf, yn, yf, conds, Q=Q, R=R)

    print(u)