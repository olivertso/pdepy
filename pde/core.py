__all__ = ['Parabolic', 'Wave']

import abc
import types
import numpy as np
from scipy import linalg

class Base(metaclass=abc.ABCMeta):
    """
    Classe base.

    Funções abstratas
    -----------------
        * solve
        * _explicit
        * _implicit
        * _set_mat
        * _set_vec
        * _cal_constants
        * _check_arguments

    Funções concretas
    -----------------
        * _set_axis
        * _set_u
        * _func_to_val
        * _check_tuple
        * _check_len
        * _check_mthd
    """

    @abc.abstractmethod
    def solve(self):
        """Função principal."""
        return

    @abc.abstractmethod
    def _explicit(self):
        """Métodos de diferenças finitas explícitos."""
        return

    @abc.abstractmethod
    def _implicit(self):
        """Métodos de diferenças finitas implícitos."""
        return

    @abc.abstractmethod
    def _set_mat(self):
        """
        Monta a matriz do sistema em cada iteração de '_implicit()'.
        """
        return

    @abc.abstractmethod
    def _set_vec(self):
        """
        Monta o vetor do sistema em cada iteração de '_implicit()'.
        """
        return

    @abc.abstractmethod
    def _cal_constants(self):
        """
        Calcula as constantes necessárias entre '𝛂', 'β' 'h' e 'k'.
        """
        return

    @abc.abstractmethod
    def _check_arguments(self):
        """Função principal para as verificações."""
        return

    def _set_axis(self, xn, xf, yn, yf):
        """Retorna os vetores dos eixos 'x' e 'y'."""
        x = np.linspace(0, xf, xn+1)
        y = np.linspace(0, yf, yn+1)

        return (x, y)

    def _set_u(self, x, y, init, bound_x0, bound_xf):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as condições
        iniciais e de contorno.
        """
        u = np.empty((len(x), len(y)))

        u[:, 0]  = self._func_to_val(init, x)
        u[0, :]  = self._func_to_val(bound_x0, y)
        u[-1, :] = self._func_to_val(bound_xf, y)

        return u

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

class Parabolic(Base):
    """
    Equação parabólica linear em derivadas parciais:
        u_y = p(x, y)*u_xx + q(x, y)*u_x + r(x, y)*u + s(x, y).

    Condições iniciais e de contorno:
        u(x, 0)  = init(x),     0 <= x <= xf,
        u(0, y)  = bound_x0(y), 0 <= y <= yf,
        u(xf, y) = bound_xf(y), 0 <= y <= yf.
    """

    def __init__(self):
        self._methods = ['ec', 'eu', 'ic', 'iu']

    def solve(self, domain, params, conds, mthd='iu'):
        """
        Métodos
        -------
            * ec: diferenças finitas centrais explícito
            * eu: diferenças finitas upwind explícito
            * ic: diferenças finitas centrais implícito
            * iu: diferenças finitas upwind implícito

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
        u      = self._set_u(*axis, *conds)

        𝛉 = self._set_𝛉(mthd)

        if mthd[0] == 'e':
            self._explicit(u, 𝛉, *consts, *params)
        elif mthd[0] == 'i':
            self._implicit(u, 𝛉, *consts, *params)

        return u

    def _explicit(self, u, 𝛉, 𝛂, β, k, p, q, r, s):
        """Métodos de diferenças finitas explícitos."""
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

    def _implicit(self, u, 𝛉, 𝛂, β, k, p, q, r, s):
        """Métodos de diferenças finitas implícitos."""
        for j in np.arange(u.shape[1]-1):
            params1 = (p[:, j], q[:, j], r[:, j])
            params2 = (p[:, j], q[:, j], s[:, j])

            mat = self._set_mat(𝛉, 𝛂, β, k, *params1)
            vec = self._set_vec(𝛉, 𝛂, β, k, *params2, u[:, j:j+2])

            u[1:-1, j+1] = linalg.solve(mat, vec)

    def _set_mat(self, 𝛉, 𝛂, β, k, p, q, r):
        """
        Monta a matriz do sistema em cada iteração de '_implicit()'.
        """
        main  = - 1 + k * r[:] - 2 * (𝛂 * p[:] + 𝛉 * β * np.abs(q[:]))
        upper = 𝛂 * p[:-1] + β * (𝛉 * np.abs(q[:-1]) + q[:-1])
        lower = 𝛂 * p[1:]  + β * (𝛉 * np.abs(q[1:])  - q[1:] )
        mat   = np.diag(main) + np.diag(upper, 1) + np.diag(lower, -1)

        return mat

    def _set_vec(self, 𝛉, 𝛂, β, k, p, q, s, u):
        """
        Monta o vetor do sistema em cada iteração de '_implicit()'.
        """
        vec      = - u[1:-1, 0] - k * s[:]
        vec[0]  -= (𝛂 * p[0]  + β * (𝛉 * np.abs(q[0])  - q[0] )) * u[0, 1]
        vec[-1] -= (𝛂 * p[-1] + β * (𝛉 * np.abs(q[-1]) + q[-1])) * u[-1, 1]

        return vec

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

    def _set_𝛉(self, mthd):
        """Retorna o valor de '𝛉' conforme 'mthd'."""
        if mthd[1] =='c':
            return 0
        elif mthd[1] == 'u':
            return 1

    def _check_arguments(self, domain, params, conds, mthd):
        """Função principal para as verificações."""
        self._check_tuple(domain, 'domain')
        self._check_len(domain, 'domain', 4)

        self._check_tuple(params, 'params')
        self._check_len(params, 'params', 4)

        self._check_tuple(conds, 'conds')
        self._check_len(conds, 'conds', 3)

        self._check_mthd(mthd)

class Wave(Base):
    """
    Equação da onda:
        u_yy = u_xx.

    Condições iniciais e de contorno:
        u(x, 0)   = init(x),     0 <= x <= xf,
        u_y(x, 0) = d_init(x),   0 <= x <= xf,
        u(0, y)   = bound_x0(y), 0 <= y <= yf,
        u(xf, y)  = bound_xf(y), 0 <= y <= yf.
    """

    def __init__(self):
        self._methods = ['e', 'i']

    def solve(self, domain, conds, mthd='i'):
        """
        Métodos
        -------
            * e: diferenças finitas explícito
            * i: diferenças finitas implícito

        Parâmetros
        ----------
        domain : tuple, (int, float, int, float)
            Tupla da forma (xn, xf, yn, yf), onde 'xn' e 'yn' são os
            números de partições nos eixos 'x' e 'y'; 'xf' e 'yf' são as
            posições finais nos eixos 'x' e 'y'.
        conds : tuple of function, scalar or array_like
            Tupla da forma (d_init, init, bound_x0, bound_xf), onde cada
            elemento pode ser uma função f(x) sendo 'x' um vetor de
            tamanho xn+1 para 'd_init' e 'init', e yn+1 para 'bound'; ou
            um escalar; ou um vetor de tamanho xn+1 para 'init' e yn+1
            para 'bound'.
        mthd : string | optional
            O método de diferenças finitas escolhido.

        Retornos
        --------
        u : ndarray
            Uma matriz de tamanho (xn+1)*(yn+1) com os resultados, onde
            cada linha representa uma posição 'x' e cada coluna representa
            um instante de tempo 'y'.
        """
        self._check_arguments(domain, conds, mthd)

        axis   = self._set_axis(*domain)
        consts = self._cal_constants(*domain)
        d_init = self._func_to_val(conds[0], axis[0])
        u      = self._set_u(*axis, *conds[1:])

        self._set_first_row(u, *consts[1:], d_init)

        if mthd == 'e':
            self._explicit(u, consts[0]**(-1))
        elif mthd == 'i':
            self._implicit(u, consts[0]**(-1))

        return u

    def _explicit(self, u, 𝛂):
        """Métodos de diferenças finitas explícitos."""
        for j in np.arange(1, u.shape[1]-1):
            u[1:-1, j+1] = 2 * u[1:-1, j] - u[1:-1, j-1] + \
                           𝛂 * (u[2:, j] - 2 * u[1:-1, j] + u[:-2, j])

    def _implicit(self, u, 𝛂):
        """Métodos de diferenças finitas implícitos."""
        mat = self._set_mat(np.shape(u)[0]-2, 𝛂)

        for j in np.arange(1, u.shape[1]-1):
            vec = self._set_vec(𝛂, u[:, j-1:j+2])

            u[1:-1, j+1] = linalg.solve(mat, vec)

    def _set_mat(self, n, 𝛂):
        """
        Monta a matriz do sistema em cada iteração de '_implicit()'.
        """
        main  = - 2 * (np.ones(n) + 𝛂)
        upper = np.ones(n-1)
        lower = np.ones(n-1)

        return np.diag(main) + np.diag(upper, 1) + np.diag(lower, -1)

    def _set_vec(self, 𝛂, u):
        """
        Monta o vetor do sistema em cada iteração de '_implicit()'.
        """
        vec = - u[:-2, 0] - u[2:, 0] + 2 * (1 + 𝛂) * u[1:-1, 0] - \
              4 * 𝛂 * u[1:-1, 1]

        vec[0]  -= u[0, 2]
        vec[-1] -= u[-1, 2]

        return vec

    def _set_first_row(self, u, h, k, d_init):
        """
        Determina a primeira linha da malha interior. 'd_init' pode ser um
        escalar ou um vetor de tamanho do 'x'.
        """
        u[1:-1, 1] = (u[:, 0] + k * d_init)[1:-1] + k**2 / 2 * \
                     (u[2:, 0] - 2 * u[1:-1, 0] + u[:-2, 0]) / (h**2)

    def _cal_constants(self, xn, xf, yn, yf):
        """Calcula as constantes '𝛂', 'h' e 'k'."""
        h = xf / xn
        k = yf / yn

        𝛂 = (k**2) / (h**2)

        return (𝛂, h, k)

    def _check_arguments(self, domain, conds, mthd):
        """Função principal para as verificações."""
        self._check_tuple(domain, 'domain')
        self._check_len(domain, 'domain', 4)

        self._check_tuple(conds, 'conds')
        self._check_len(conds, 'conds', 4)

        self._check_mthd(mthd)

def _test_parabolic():
    xn = 4
    xf = 4.
    yn = 2
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
    mthd   = 'iu'

    u = Parabolic().solve(domain, params, conds, mthd=mthd)

    print(u)

def _test_wave():
    xn = 4
    xf = 1.
    yn = 4
    yf = 0.5

    d_init = 1
    init   = lambda x: x * (1 - x)
    bound1 = lambda y: y * (1 - y)
    bound2 = lambda y: y * (1 - y)

    domain = (xn, xf, yn, yf)
    conds  = (d_init, init, bound1, bound2)
    mthd   = 'i'

    u = Wave().solve(domain, conds, mthd=mthd)

    print(u)

if __name__ == '__main__':
    _test_parabolic()
    print()
    _test_wave()