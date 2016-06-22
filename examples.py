import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from pde import laplace
from pde import parabolic
from pde import wave

def surface(u, x, y):
    """3d surface plot."""
    fig = plt.figure()
    ax  = fig.gca(projection='3d')

    y_mesh, x_mesh = np.meshgrid(y, x)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('u')
    ax.plot_trisurf(x_mesh.flatten(), y_mesh.flatten(), u.flatten(),
                    cmap=cm.jet, linewidth=0.2)

    plt.show()

def plot_laplace():
    xn = 30
    xf = 3.
    yn = 40
    yf = 4.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    f = lambda x, y: (x-1)**2 - (y-2)**2
    bound_x0 = f(0, y)
    bound_xf = f(xf, y)
    bound_y0 = f(x, 0)
    bound_yf = f(x, yf)

    axis  = (x, y)
    conds = (bound_x0, bound_xf, bound_y0, bound_yf)

    surface(laplace.solve(axis, conds, method='ic'), x, y)

def plot_parabolic():
    xn = 40
    xf = 4.
    yn = 50
    yf = 0.5

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    init   = (lambda x: x**2 - 4*x + 5)(x)
    bound1 = (lambda y: 5 * np.exp(-y))(y)
    bound2 = (lambda y: 5 * np.exp(-y))(y)

    p = 1
    q = 1
    r = -3
    s = 3

    axis   = (x, y)
    conds  = (init, bound1, bound2)
    params = (p, q, r, s)

    surface(parabolic.solve(axis, params, conds, method='iu'), x, y)

def plot_wave():
    xn = 40
    xf = 1.
    yn = 40
    yf = 1.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    d_init = 1
    init   = (lambda x: x * (1-x))(x)
    bound1 = (lambda y: y * (1-y))(y)
    bound2 = (lambda y: y * (1-y))(y)

    axis  = (x, y)
    conds = (d_init, init, bound1, bound2)

    surface(wave.solve(axis, conds, method='i'), x, y)

plot_laplace()
plot_parabolic()
plot_wave()
