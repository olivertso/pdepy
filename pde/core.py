__all__ = ['laplace', 'parabolic', 'wave']

import abc, sys, types
import numpy as np
from scipy import linalg

def laplace(domain, conds, mthd='c'):
    return Laplace().solve(domain, conds, mthd)

def parabolic(domain, params, conds, mthd='iu'):
    return Parabolic().solve(domain, params, conds, mthd)

def wave(domain, conds, mthd='i'):
    return Wave().solve(domain, conds, mthd)

class Base(abc.ABC):
    """
    Classe base.

    Funções abstratas
    -----------------
        * solve
        * _implicit
        * _set_mat
        * _set_vec
        * _set_u
        * _cal_constants
        * _mesh_int_grid

    Funções concretas
    -----------------
        * _set_axis
        * _set_parameters
        * _check_mthd
    """

    @abc.abstractmethod
    def solve(self):
        """Função principal."""
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
    def _set_u(self):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as condições
        oferecidas.
        """
        return

    @abc.abstractmethod
    def _cal_constants(self):
        """
        Calcula as constantes necessárias.
        """
        return

    @abc.abstractmethod
    def _mesh_int_grid(self):
        """
        Retorna matrizes 'x' e 'y' conforme o tamanho da malha interior.
        """
        return

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
        _params = list(params)

        for i in np.arange(len(_params)):
            if isinstance(_params[i], types.FunctionType):
                y_m, x_m = self._mesh_int_grid(y, x)
                _params[i] = _params[i](x_m, y_m)

            elif isinstance(_params[i], (int, float)):
                _params[i] *= np.ones((len(x)-2, len(y)-1))

        return _params

    def _check_mthd(self, mthd):
        """Verifica se o método numérico 'mthd' é válido."""
        if mthd not in self._methods:
            sys.exit('Value \'' + mthd + '\' for argument \'mthd\' is '
                     'not valid.')

class TimeDependent(Base):
    """
    Classe base para equações diferenciais parciais dependente de uma
    variável temporal.

    Funções abstratas
    -----------------
        * _explicit

    Funções concretas
    -----------------
        * _set_u
        * _mesh_int_grid
    """

    @abc.abstractmethod
    def _explicit(self):
        """Métodos de diferenças finitas explícitos."""
        return

    def _set_u(self, xn, yn, init, bound_x0, bound_xf):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as condições
        iniciais e de contorno.
        """
        u = np.empty((xn+1, yn+1))

        u[:, 0]  = init
        u[0, :]  = bound_x0
        u[-1, :] = bound_xf

        return u

    def _mesh_int_grid(self, y, x):
        """
        Retorna matrizes 'x' e 'y' de tamanho (xn-2)*(yn-1).
        """
        return np.meshgrid(y[:-1], x[1:-1])

class SteadyState(Base):
    """
    Classe base para equações diferenciais parciais em estados
    estacionários.

    Funções concretas
    -----------------
        * _set_u
        * _mesh_int_grid
    """

    def _set_u(self, xn, yn, bound_x0, bound_xf, bound_y0, bound_yf):
        """
        Inicializa a matriz 'u' de tamanho (xn+1)*(yn+1) com as condições
        de contorno.
        """
        u = np.empty((xn+1, yn+1))

        u[0, :]  = bound_x0
        u[-1, :] = bound_xf
        u[:, 0]  = bound_y0
        u[:, -1] = bound_yf

        return u

    def _mesh_int_grid(self, y, x):
        """
        Retorna matrizes 'x' e 'y' de tamanho (xn-2)*(yn-2).
        """
        return np.meshgrid(y[1:-1], x[1:-1])

class Laplace(SteadyState):
    """
    Equação de Laplace:
        u_xx + u_yy = 0.

    Condições de contorno:
        u(x, y) = bound(x, y), (x, y) pertencente ao contorno.
    """

    def __init__(self):
        self._methods = ['c']

    def solve(self, domain, conds, mthd):
        """
        Métodos
        -------
            * c: diferenças finitas centrais
            * TODO: u: diferenças finitas upwind

        Parâmetros
        ----------
        domain : tuple, (int, float, int, float)
            Tupla da forma (xn, xf, yn, yf), onde 'xn' e 'yn' são os
            números de partições nos eixos 'x' e 'y'; 'xf' e 'yf' são as
            posições finais nos eixos 'x' e 'y'.
        conds : tuple of scalar or array_like
            Tupla da forma (bound_x0, bound_xf, bound_y0, bound_yf), onde
            cada elemento pode ser um escalar, ou um vetor de tamanho xn+1
            para 'cond_x' e yn+1 para 'cond_y'.
        mthd : string | optional
            O método de diferenças finitas escolhido.

        Retornos
        --------
        u : ndarray
            Uma matriz de tamanho (xn+1)*(yn+1) com os resultados, onde
            cada linha representa uma posição 'x' e cada coluna representa
            um instante de tempo 'y'.
        """
        self._check_mthd(mthd)

        consts = self._cal_constants(*domain)
        u      = self._set_u(*domain[::2], *conds)

        self._implicit(u, *domain[::2], *consts)

        return u

    def _implicit(self, u, xn, yn, 𝛂, β):
        """Métodos de diferenças finitas implícitos."""
        mat = self._set_mat(𝛂, β, xn, yn)
        vec = self._set_vec(𝛂, β, u)

        x = linalg.solve(mat, vec)

        u[1:-1, 1:-1] = np.reshape(x, (xn-1, yn-1), 'F')

    def _set_mat(self, 𝛂, β, xn, yn):
        """Monta a matriz do sistema em '_implicit()'."""
        n = (xn-1) * (yn-1)

        main = np.full(n, - 2 * (𝛂 + β))
        sub1 = np.full(n-1, β)
        sub2 = np.full(n-xn+1, 𝛂)

        sub1[xn-2:-1:xn-1] = 0

        return np.diag(main) + np.diag(sub1, 1) + np.diag(sub1, -1) + \
               np.diag(sub2, xn-1) + np.diag(sub2, -xn+1)

    def _set_vec(self, 𝛂, β, u):
        """Monta o vetor do sistema em '_implicit()'."""
        vec = np.zeros_like((u[1:-1, 1:-1]))

        vec[0, :]  -= β * u[0, 1:-1]
        vec[-1, :] -= β * u[-1, 1:-1]
        vec[:, 0]  -= 𝛂 * u[1:-1, 0]
        vec[:, -1] -= 𝛂 * u[1:-1, -1]

        return np.reshape(vec, np.size(vec), 'F')

    def _cal_constants(self, xn, xf, yn, yf):
        """Calcula as constantes '𝛂' e 'β'."""
        𝛂 = (xf / xn)**2
        β = (yf / yn)**2

        return (𝛂, β)

class Parabolic(TimeDependent):
    """
    Equação parabólica linear em derivadas parciais:
        u_y = p(x, y)*u_xx + q(x, y)*u_x + r(x, y)*u + s(x, y).

    Condições iniciais e de contorno:
        u(x, 0)  = init(x),     0 <= x <= xf,
        u(0, y)  = bound_x0(y), 0 <= y <= yf,
        u(xf, y) = bound_xf(y), 0 <= y <= yf.

    Funções próprias
    ----------------
        * _set_𝛉
    """

    def __init__(self):
        self._methods = ['ec', 'eu', 'ic', 'iu']

    def solve(self, domain, params, conds, mthd):
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
        conds : tuple of scalar or array_like
            Tupla da forma (init, bound_x0, bound_xf), onde cada elemento
            pode ser uma um escalar; ou um vetor de tamanho xn+1 para
            'init' e yn+1 para 'bound'.
        mthd : string | optional
            O método de diferenças finitas escolhido.

        Retornos
        --------
        u : ndarray
            Uma matriz de tamanho (xn+1)*(yn+1) com os resultados, onde
            cada linha representa uma posição 'x' e cada coluna representa
            um instante de tempo 'y'.
        """
        self._check_mthd(mthd)

        axis   = self._set_axis(*domain)
        params = self._set_parameters(params, *axis)
        consts = self._cal_constants(*domain)
        u      = self._set_u(*domain[::2], *conds)

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

        return np.diag(main) + np.diag(upper, 1) + np.diag(lower, -1)

    def _set_vec(self, 𝛉, 𝛂, β, k, p, q, s, u):
        """
        Monta o vetor do sistema em cada iteração de '_implicit()'.
        """
        vec      = - u[1:-1, 0] - k * s[:]
        vec[0]  -= (𝛂 * p[0]  + β * (𝛉 * np.abs(q[0])  - q[0] )) * u[0, 1]
        vec[-1] -= (𝛂 * p[-1] + β * (𝛉 * np.abs(q[-1]) + q[-1])) * u[-1, 1]

        return vec

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

class Wave(TimeDependent):
    """
    Equação da onda:
        u_yy = u_xx.

    Condições iniciais e de contorno:
        u(x, 0)   = init(x),     0 <= x <= xf,
        u_y(x, 0) = d_init(x),   0 <= x <= xf,
        u(0, y)   = bound_x0(y), 0 <= y <= yf,
        u(xf, y)  = bound_xf(y), 0 <= y <= yf.

    Funções próprias
    ----------------
        * _set_first_row
    """

    def __init__(self):
        self._methods = ['e', 'i']

    def solve(self, domain, conds, mthd):
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
        conds : tuple of scalar or array_like
            Tupla da forma (d_init, init, bound_x0, bound_xf), onde cada
            elemento pode ser um escalar; ou um vetor de tamanho xn+1 para
            'init' e yn+1 para 'bound'.
        mthd : string | optional
            O método de diferenças finitas escolhido.

        Retornos
        --------
        u : ndarray
            Uma matriz de tamanho (xn+1)*(yn+1) com os resultados, onde
            cada linha representa uma posição 'x' e cada coluna representa
            um instante de tempo 'y'.
        """
        self._check_mthd(mthd)

        consts = self._cal_constants(*domain)
        u      = self._set_u(*domain[::2], *conds[1:])

        self._set_first_row(u, *consts[1:], conds[0])

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

    def _cal_constants(self, xn, xf, yn, yf):
        """Calcula as constantes '𝛂', 'h' e 'k'."""
        h = xf / xn
        k = yf / yn

        𝛂 = (k**2) / (h**2)

        return (𝛂, h, k)

    def _set_first_row(self, u, h, k, d_init):
        """
        Determina a primeira linha da malha interior. 'd_init' pode ser um
        escalar ou um vetor de tamanho do 'x'.
        """
        u[1:-1, 1] = (u[:, 0] + k * d_init)[1:-1] + k**2 / 2 * \
                     (u[2:, 0] - 2 * u[1:-1, 0] + u[:-2, 0]) / (h**2)

def _test_laplace():
    xn = 3
    xf = 3.
    yn = 4
    yf = 4.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    f = lambda x, y: (x - 1)**2 - (y - 2)**2
    bound_x0 = f(0, y)
    bound_xf = f(xf, y)
    bound_y0 = f(x, 0)
    bound_yf = f(x, yf)

    domain = (xn, xf, yn, yf)
    conds  = (bound_x0, bound_xf, bound_y0, bound_yf)
    mthd   = 'c'

    u = laplace(domain, conds, mthd=mthd)

    print(u)

def _test_parabolic():
    xn = 4
    xf = 4.
    yn = 2
    yf = 1.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    p = 1
    q = lambda x, y: x - 2.
    r = -3
    s = 0

    init   = (lambda x: x**2 - 4*x + 5)(x)
    bound1 = (lambda y: 5 * np.exp(-y))(y)
    bound2 = (lambda y: 5 * np.exp(-y))(y)

    domain = (xn, xf, yn, yf)
    params = (p, q, r, s)
    conds  = (init, bound1, bound2)
    mthd   = 'iu'

    u = parabolic(domain, params, conds, mthd=mthd)

    print(u)

def _test_wave():
    xn = 4
    xf = 1.
    yn = 4
    yf = 0.5

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    d_init = 1
    init   = (lambda x: x * (1 - x))(x)
    bound1 = (lambda y: y * (1 - y))(y)
    bound2 = (lambda y: y * (1 - y))(y)

    domain = (xn, xf, yn, yf)
    conds  = (d_init, init, bound1, bound2)
    mthd   = 'i'

    u = wave(domain, conds, mthd=mthd)

    print(u)

if __name__ == '__main__':
    _test_laplace()
    print()
    _test_parabolic()
    print()
    _test_wave()