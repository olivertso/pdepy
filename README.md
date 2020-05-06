# PDEPy

[![Supported Python versions](https://img.shields.io/pypi/pyversions/pytest.svg)](https://pypi.org/project/pdepy/)
[![PyPI version](https://badge.fury.io/py/pdepy.svg)](https://badge.fury.io/py/pdepy)
[![Build Status](https://travis-ci.org/olivertso/pdepy.svg?branch=master)](https://travis-ci.org/olivertso/pdepy)
[![Coverage Status](https://coveralls.io/repos/github/olivertso/pdepy/badge.svg?branch=master)](https://coveralls.io/github/olivertso/pdepy?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A Python 3 library for solving initial and boundary value problems of some linear partial differential equations using finite-difference methods.

- Laplace
    - Implicit Central
- Parabolic
    - Explicit Central
    - Explicit Upwind
    - Implicit Central
    - Implicit Upwind
- Wave
    - Explicit
    - Implicit

## Usage

### Installation

```
pip install pdepy
```

### Examples

#### Laplace's Equation

```python
import numpy as np
from pdepy import laplace

xn, xf, yn, yf = 30, 3.0, 40, 4.0

x = np.linspace(0, xf, xn + 1)
y = np.linspace(0, yf, yn + 1)

f = lambda x, y: (x - 1) ** 2 - (y - 2) ** 2
bound_x0 = f(0, y)
bound_xf = f(xf, y)
bound_y0 = f(x, 0)
bound_yf = f(x, yf)

axis = (x, y)
conds = (bound_x0, bound_xf, bound_y0, bound_yf)

laplace.solve(axis, conds, method="ic")
```

#### Parabolic Equation

```python
import numpy as np
from pdepy import parabolic

xn, xf, yn, yf = 40, 4.0, 50, 0.5

x = np.linspace(0, xf, xn + 1)
y = np.linspace(0, yf, yn + 1)

init = x ** 2 - 4 * x + 5
bound = 5 * np.exp(-y)

p, q, r, s = 1, 1, -3, 3

axis = (x, y)
conds = (init, bound, bound)
params = (p, q, r, s)

parabolic.solve(axis, params, conds, method="iu")
```

#### Wave Equation

```python
import numpy as np
from pdepy import wave

xn, xf, yn, yf = 40, 1.0, 40, 1.0

x = np.linspace(0, xf, xn + 1)
y = np.linspace(0, yf, yn + 1)

d_init = 1
init = x * (1 - x)
bound = y * (1 - y)

axis = (x, y)
conds = (d_init, init, bound, bound)

wave.solve(axis, conds, method="i")
```

## Development

Create virtual environment and install requirements:
```
bin/setup_venv
```

### Other commands

Run command in virtual environment:
```
bin/run <command>
```

Install requirements:
```
bin/install_requirements
```

Format codebase:
```
bin/format
```

Lint codebase:
```
bin/lint
```

Run unit tests:
```
bin/test
```

## Publish

Package and distribute:
```
bin/publish
```
