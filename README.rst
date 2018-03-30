=====
PDEPy
=====

.. image:: https://img.shields.io/pypi/v/pdepy.svg
    :target: https://pypi.org/project/pdepy/

.. image:: https://travis-ci.org/olivertso/pdepy.svg?branch=master
    :target: https://travis-ci.org/olivertso/pdepy

.. image:: https://coveralls.io/repos/github/olivertso/pdepy/badge.svg?branch=master
    :target: https://coveralls.io/github/olivertso/pdepy?branch=master

Overview
--------

**Disclaimer: Use at your own risk. I have a bachelor's degree in applied and computational mathematics, but never worked professionally in the field.**

A python 3 library for solving initial and boundary value problems of some linear partial differential equations using finite-difference methods:

-  Laplace

   -  implicit central

-  Parabolic

   -  explicit central
   -  explicit upwind
   -  implicit central
   -  implicit upwind

-  Wave

   -  explicit
   -  implicit

Getting Started
---------------

Installing
""""""""""

::

    pip install pdepy

Examples
""""""""

**Laplace's Equation:**

.. code-block:: python

    import numpy as np
    from pdepy import laplace

    xn, xf, yn, yf = 30, 3., 40, 4.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    f = lambda x, y: (x-1)**2 - (y-2)**2
    bound_x0 = f(0, y)
    bound_xf = f(xf, y)
    bound_y0 = f(x, 0)
    bound_yf = f(x, yf)

    axis  = (x, y)
    conds = (bound_x0, bound_xf, bound_y0, bound_yf)

    laplace.solve(axis, conds, method='ic')

**Parabolic Equation:**

.. code-block:: python

    import numpy as np
    from pdepy import parabolic

    xn, xf, yn, yf = 40, 4., 50, 0.5

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    init  = x**2 - 4*x + 5
    bound = 5 * np.exp(-y)

    p, q, r, s = 1, 1, -3, 3

    axis   = (x, y)
    conds  = (init, bound, bound)
    params = (p, q, r, s)

    parabolic.solve(axis, params, conds, method='iu')

**Wave Equation:**

.. code-block:: python

    import numpy as np
    from pdepy import wave

    xn, xf, yn, yf = 40, 1., 40, 1.

    x = np.linspace(0, xf, xn+1)
    y = np.linspace(0, yf, yn+1)

    d_init = 1
    init   = x * (1-x)
    bound  = y * (1-y)

    axis  = (x, y)
    conds = (d_init, init, bound, bound)

    wave.solve(axis, conds, method='i')

Developing and Testing
----------------------

::

    pip install tox
    pip install -e .

    # Testing.
    tox

    # Always remove .tox/ after changing the files in ./requirements.
    rm -rf .tox/


Packaging and Distributing
--------------------------

Do not forget to update the :code:`version` field in :code:`setup.py`.

::

    pip install twine

    # Packaging.
    python setup.py sdist
    python setup.py bdist_wheel

    # Distributing.
    twine upload dist/*

More about packaging and distributing `here <https://packaging.python.org/tutorials/distributing-packages/>`_.
