# PDE

A python 3 library for solving initial and boundary value problems of some linear partial differential equations using finite-difference methods.

* Laplace
  * implicit central
* Parabolic
  * explicit central
  * explicit upwind
  * implicit central
  * implicit upwind
* Wave
  * explicit
  * implicit

## Examples

```
>>> import numpy as np
>>> from pde import wave
>>> x = np.linspace(0, 1., 5)
>>> y = np.linspace(0, 1., 5)
>>> d_init = 1.
>>> init = x * (1-x)
>>> bound = y * (1-y)
>>> wave.solve((x, y), (d_init, init, bound, bound), method='e')
array([[ 0.    ,  0.1875,  0.25  ,  0.1875,  0.    ],
       [ 0.1875,  0.375 ,  0.4375,  0.375 ,  0.1875],
       [ 0.25  ,  0.4375,  0.5   ,  0.4375,  0.25  ],
       [ 0.1875,  0.375 ,  0.4375,  0.375 ,  0.1875],
       [ 0.    ,  0.1875,  0.25  ,  0.1875,  0.    ]])
```

More in examples.py.

 Laplace | Parabolic | Wave
:-------:|:---------:|:----:
![Alt text](/img/fig_laplace.png?raw=true "fig_laplace") | ![Alt text](/img/fig_parabolic.png?raw=true "fig_parabolic") | ![Alt text](/img/fig_wave.png?raw=true "fig_wave")
