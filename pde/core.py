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
    domain : list of int/float
        [xn, xf, yn, yf], onde 'xn' é inteiro, o número de pontos no
        eixo 'x' menos 1, 'xf' é escalar, a posição final no eixo x,
        e analogamente para 'yn' e 'yf'.
    params : list of function, scalar, array_like
        Os parâmetros P, Q, R e S. Cada um pode ser uma função vetorial
        de duas variáveis, ou um escalar, ou uma matriz de tamanho
        (xn-1)*yn.
    conds : list of function, scalar, array_like
        'conds[0]' é as condições iniciais, 'conds[1]' e 'conds[2]'
        são as condições de contornos em x=0 e 'xf', respectivamente.
        Cada elemento de 'conds' pode ser uma função vetorial de uma
        variável, ou um escalar, ou um vetor de tamanho 'xn+1' ou
        'yn+1'.
    mthd : string | optional
        Método para resolver a equação. 'ec' para diferenças finitas
        centrais explícito.

    Retornos
    --------
    u : ndarray
        Uma matriz de tamanho (xn+1)*(yn+1) com os resultados,
        onde cada linha representa uma posição 'x' e cada coluna
        representa uma instante de tempo 'y'.
    """

    def solve(self, domain, params, conds, mthd='ec'):
        """
        Método principal. Inicializa os parâmetros e chama o método
        especificado para resolver a equação.
        """
        x, y    = self.cal_axis(*domain)
        𝛂, β, k = self.cal_constants(*domain)
        u       = self.init_u(x, y, conds)

        self.set_parameters(params, x, y)

        if mthd == 'ec':
            self.ec(u, 𝛂, β, k, *params)
        else:
            u = 0

        return u

    def ec(self, u, 𝛂, β, k, P, Q, R, S):
        """
        Diferenças finitas centrais explícito.
        """
        for j in np.arange(u.shape[1]-1):
            u[1:-1, j+1] = (𝛂 * P[:, j] - β * Q[:, j]) * u[:-2, j] + \
                           (𝛂 * P[:, j] + β * Q[:, j]) * u[2:, j] + \
                           (1 + k * R[:, j] - 2 * 𝛂 * P[:, j]) * u[1:-1, j] + \
                           k * S[:, j]

    def cal_axis(self, xn, xf, yn, yf):
        """Retorna os vetores dos eixos 'x' e 'y'."""
        x = np.linspace(0, xf, xn+1)
        y = np.linspace(0, yf, yn+1)

        return x, y

    def cal_constants(self, xn, xf, yn, yf):
        """Calcula as constantes '𝛂', 'β' e 'k'."""
        h = xf / xn
        k = yf / yn

        𝛂 = k / h**2
        β = k / (2 * h)

        return 𝛂, β, k

    def init_u(self, x, y, conds):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as
        condições iniciais e de contornos.
        """
        u = np.empty((len(x), len(y)))
        self.set_conditions(u, conds, x, y)

        return u

    def set_parameters(self, params, x, y):
        """
        Verifica o tipo de cada parâmetro, se for do tipo function,
        aplica as variáveis de 'x' e 'y'.
        """
        for i in range(len(params)):
            params[i] = self.func_to_val(params[i], x, y)

    def set_conditions(self, u, conds, x, y):
        """
        Verifica o tipo de cada condições iniciais e de contornos,
        se for do tipo function, aplica os valores de 'x' ou 'y', e
        atualiza a matriz 'u'.
        """
        u[:, 0]  = self.func_to_val(conds[0], x)
        u[0, :]  = self.func_to_val(conds[1], y)
        u[-1, :] = self.func_to_val(conds[2], y)

    def func_to_val(self, func_or_val, *args):
        """
        Se 'func_or_val' for uma função, aplica os valores de 'args',
        se for um escalar, retorna uma matriz com valores desse escalar,
        se for um vetor ou uma matriz, retorna sem modificar.
        """
        if isinstance(func_or_val, types.FunctionType):
            if len(args) == 2:
                args = np.meshgrid(args[1][:-1], args[0][1:-1])

            return func_or_val(*args[::-1])

        elif isinstance(func_or_val, (int, float)) and len(args) == 2:
            x = np.ones((len(args[0])-2, len(args[1])-1))

            return func_or_val * x

        else:
            return func_or_val

def _test():
    xn = 4
    xf = 4.
    yn = 10
    yf = 1.

    P = 1
    Q = lambda x, y: x - 2.
    R = -3
    S = 0

    init   = lambda x: x**2 - 4*x + 5
    bound1 = lambda y: 5 * np.exp(-y)
    bound2 = lambda y: 5 * np.exp(-y)

    domain = [xn, xf, yn, yf]
    params = [P, Q, R, S]
    conds  = [init, bound1, bound2]

    u = LinParabolic().solve(domain, params, conds)

    print(u)

if __name__ == '__main__':
    _test()