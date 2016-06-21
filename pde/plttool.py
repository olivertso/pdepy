"""
Functions for plotting 3d grafics.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

__all__ = ['surface']

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
