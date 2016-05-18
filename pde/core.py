__all__ = ['Parabolic']

import types
import numpy as np

class Parabolic(object):
    """
    Equação parabólica linear:
        u_t = p(x, y)*u_xx + q(x, y)*u_x + r(x, y)*u + s(x, y).

    Condições iniciais e de contornos:
        u(x, 0)  = init(x),     0 <= x <= xf,
        u(0, y)  = bound_x0(y), 0 <= y <= yf,
        u(xf, y) = bound_xf(y), 0 <= y <= yf.
    """

    def solve(self, domain, params, conds, mthd='ec'):
        """
        Métodos
        -------
            * Diferenças finitas centrais explícito

        Parâmetros
        ----------
        domain : tuple of int/float
            (xn, xf, yn, yf), onde 'xn' é inteiro, o número de pontos no
            eixo 'x' da malha interior, 'xf' é escalar, a posição final
            final no eixo x, e analogamente para 'yn' e 'yf'.
        params : tuple of function, scalar, array_like
            (p, q, r, s), onde cada elemento pode ser uma função de duas
            variáveis (vetor/matriz), ou um escalar, ou uma matriz de
            tamanho (xn-1)*yn.
        conds : tuple of function, scalar, array_like
            (init, bound_x0, bound_xf), onde cada elemento pode ser uma
            função de uma variável, ou um escalar, ou um vetor de tamanho
            'xn+1' para 'init' e 'yn+1' para 'bound'.
        mthd : string | optional
            O método escolhido. 'ec' para diferenças finitas centrais
            explícito.

        Retornos
        --------
        u : ndarray
            Uma matriz de tamanho (xn+1)*(yn+1) com os resultados, onde
            cada linha representa uma posição 'x' e cada coluna representa
            um instante de tempo 'y'.
        """
        axis   = self._set_axis(*domain)
        params = self._set_parameters(params, *axis)
        consts = self._cal_constants(*domain)
        u      = self._set_u(*axis, conds)

        if mthd == 'ec':
            self._ec(u, *consts, *params)
        else:
            u = 0

        return u

    def _ec(self, u, 𝛂, β, k, p, q, r, s):
        """Diferenças finitas centrais explícito."""
        for j in np.arange(u.shape[1]-1):
            u[1:-1, j+1] = (𝛂 * p[:, j] - β * q[:, j]) * u[:-2, j] + \
                           (𝛂 * p[:, j] + β * q[:, j]) * u[2:, j] + \
                           (1 + k * r[:, j] - 2 * 𝛂 * p[:, j]) * u[1:-1, j] + \
                           k * s[:, j]

    def _set_axis(self, xn, xf, yn, yf):
        """Retorna os vetores dos eixos 'x' e 'y'."""
        x = np.linspace(0, xf, xn+1)
        y = np.linspace(0, yf, yn+1)

        return (x, y)

    def _set_parameters(self, params, x, y):
        """
        Atualiza os parâmetros para matrizes de tamanho da malha interior
        de 'u'.
        """
        _params = []

        for param in params:
            _params.append(self._func_to_val(param, x, y))

        return _params

    def _cal_constants(self, xn, xf, yn, yf):
        """Calcula as constantes '𝛂', 'β' e 'k'."""
        h = xf / xn
        k = yf / yn

        𝛂 = k / h**2
        β = k / (2 * h)

        return (𝛂, β, k)

    def _set_u(self, x, y, conds):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as condições
        iniciais e de contornos.
        """
        u = np.empty((len(x), len(y)))
        self._set_conditions(u, *conds, x, y)

        return u

    def _set_conditions(self, u, init, bound_x0, bound_xf, x, y):
        """
        Atualiza a matriz 'u' com as condições iniciais e de contornos.
        """
        u[:, 0]  = self._func_to_val(init, x)
        u[0, :]  = self._func_to_val(bound_x0, y)
        u[-1, :] = self._func_to_val(bound_xf, y)

    def _func_to_val(self, func_or_val, *axis):
        """Retorna os 'params' ou 'conds' no formato certo."""
        if isinstance(func_or_val, types.FunctionType):
            if len(axis) == 2:
                # Caso dos parâmetros 'p', 'q', 'r' e 's'. Vetores 'x' e
                # 'y' são transformados em matrizes do tamanho da malha
                # interior.
                axis = np.meshgrid(axis[1][:-1], axis[0][1:-1])[::-1]

            # Se len(axis)=1 então é caso das condições, os vetores 'x' e
            # 'y' não são modificados.

            return func_or_val(*axis)

        elif isinstance(func_or_val, (int, float)) and len(axis) == 2:
            # Caso dos parâmetros 'p', 'q', 'r' e 's'.
            x = np.ones((len(axis[0])-2, len(axis[1])-1))

            return func_or_val * x

        else:
            # Se 'func_or_val' é escalar e len(axis)=1, é caso das
            # condições, 'func_or_val' não é modificada.
            return func_or_val

def _test():
    xn = 4
    xf = 4.
    yn = 10
    yf = 1.

    p = 1
    q = lambda x, y: x - 2.
    r = -3
    s = 0

    init   = lambda x: x**2 - 4*x + 5
    bound1 = lambda y: 5 * np.exp(-y)
    bound2 = lambda y: 5 * np.exp(-y)

    domain = (xn, xf, yn, yf)
    params = (p, q, r, s)
    conds  = (init, bound1, bound2)

    u = Parabolic().solve(domain, params, conds)

    print(u)

if __name__ == '__main__':
    _test()