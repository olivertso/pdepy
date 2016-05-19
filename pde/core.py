__all__ = ['Parabolic']

import types
import numpy as np

class Parabolic(object):
    """
    Equação parabólica linear em derivadas parciais:
        u_t = p(x, y)*u_xx + q(x, y)*u_x + r(x, y)*u + s(x, y).

    Condições iniciais e de contorno:
        u(x, 0)  = init(x),     0 <= x <= xf,
        u(0, y)  = bound_x0(y), 0 <= y <= yf,
        u(xf, y) = bound_xf(y), 0 <= y <= yf.
    """

    def __init__(self):
        self._methods = ['ec', 'eu']

    def solve(self, domain, params, conds, mthd='ec'):
        """
        Métodos
        -------
            * ec: diferenças finitas centrais explícito
            * eu: diferenças finitas upwind explícito

        Parâmetros
        ----------
        domain : tuple, (int, float, int, float)
            Tupla da forma (xn, xf, yn, yf), onde 'xn' e 'yn' são os
            números de partições nos eixos 'x' e 'y'; 'xf' e 'yf' são as
            posições finais nos eixos 'x' e 'y'.
        params : tuple of function, scalar or array_like
            Tupla da forma (p, q, r, s), onde cada elemento pode ser uma
            função f(x, y) sendo 'x' e 'y' matrizes de tamanho (xn-1)*yn;
            ou um escalar; ou uma matriz de tamanho (xn-1)*yn.
        conds : tuple of function, scalar or array_like
            Tupla da forma (init, bound_x0, bound_xf), onde cada elemento
            pode ser uma função f(x) sendo 'x' um vetor de tamanho xn+1
            para 'init' e yn+1 para 'bound'; ou um escalar; ou um vetor
            de tamanho xn+1 para 'init' e yn+1 para 'bound'.
        mthd : string | optional
            O método de diferenças finitas escolhido.

        Retornos
        --------
        u : ndarray
            Uma matriz de tamanho (xn+1)*(yn+1) com os resultados, onde
            cada linha representa uma posição 'x' e cada coluna representa
            um instante de tempo 'y'.
        """
        self._check_arguments(domain, params, conds, mthd)

        axis   = self._set_axis(*domain)
        params = self._set_parameters(params, *axis)
        consts = self._cal_constants(*domain)
        u      = self._set_u(*axis, conds)

        if mthd[0] == 'e':
            if mthd[1] =='c':
                𝛉 = 0
            elif mthd[1] == 'u':
                𝛉 = 1

            self._explicit(u, 𝛉, *consts, *params)

        return u

    def _explicit(self, u, 𝛉, 𝛂, β, k, p, q, r, s):
        """Diferenças finitas centrais(𝛉=0)/upwind(𝛉=1) explícito."""
        for j in np.arange(u.shape[1]-1):
            u[1:-1, j+1] = (𝛂 * p[:, j] + \
                           β * (𝛉 * np.abs(q[:, j]) - q[:, j])) * \
                           u[:-2, j] + \
                           (𝛂 * p[:, j] + \
                           β * (𝛉 * np.abs(q[:, j]) + q[:, j])) * \
                           u[2:, j] + \
                           (1 + k * r[:, j] - \
                           2 * (𝛂 * p[:, j] + 𝛉 * β * np.abs(q[:, j]))) * \
                           u[1:-1, j] + \
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
        iniciais e de contorno.
        """
        u = np.empty((len(x), len(y)))
        self._set_conditions(u, *conds, x, y)

        return u

    def _set_conditions(self, u, init, bound_x0, bound_xf, x, y):
        """
        Atualiza a matriz 'u' com as condições iniciais e de contorno.
        """
        u[:, 0]  = self._func_to_val(init, x)
        u[0, :]  = self._func_to_val(bound_x0, y)
        u[-1, :] = self._func_to_val(bound_xf, y)

    def _func_to_val(self, func_or_val, *axis):
        """
        Retorna elemento de 'params' como matriz ou de 'conds' como vetor.
        """
        if isinstance(func_or_val, types.FunctionType):
            if len(axis) == 2:
                # Caso dos parâmetros. Vetores 'x' e 'y' são transformados
                # em matrizes do tamanho da malha interior.
                axis = np.meshgrid(axis[1][:-1], axis[0][1:-1])[::-1]

            # Se len(axis)=1 então é caso das condições, os vetores 'x' e
            # 'y' não são modificados.

            return func_or_val(*axis)

        elif isinstance(func_or_val, (int, float)) and len(axis) == 2:
            # Caso dos parâmetros. Uma matriz do tamanho da malha interior
            # é criada.
            x = np.ones((len(axis[0])-2, len(axis[1])-1))

            return func_or_val * x

        else:
            # Se 'func_or_val' é escalar e len(axis)=1, é caso das
            # condições, 'func_or_val' não é modificada.
            return func_or_val

    def _check_arguments(self, domain, params, conds, mthd):
        """Função principal para as verificações."""
        self._check_tuple(domain, 'domain')
        self._check_len(domain, 'domain', 4)

        self._check_tuple(params, 'params')
        self._check_len(params, 'params', 4)

        self._check_tuple(conds, 'conds')
        self._check_len(conds, 'conds', 3)

        self._check_mthd(mthd)

    def _check_tuple(self, arg, arg_name):
        """Verifica se 'arg' é do tipo tupla."""
        if not isinstance(arg, tuple):
            raise TypeError('\'' + arg_name + '\' should be a tuple.')

    def _check_len(self, arg, arg_name, exp_len):
        """Verifica se 'arg' tem tamanho 'exp_len'."""
        if len(arg) != exp_len:
            raise ValueError('\'' + arg_name + '\' should have ' + \
                             str(exp_len) + ' elements, ' + \
                             str(len(arg)) + ' given.')

    def _check_mthd(self, mthd):
        """Verifica se o método numérico 'mthd' é válido."""
        if mthd not in self._methods:
            raise ValueError('Method \'' + mthd + '\' is not valid.')

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
    mthd   = 'eu'

    u = Parabolic().solve(domain, params, conds, mthd=mthd)

    print(u)

if __name__ == '__main__':
    _test()