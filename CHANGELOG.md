# Change Log

## v0.1.1 (2016-05-15)
**Fixed**
* Em `Heat1D().exp_central()`, multiplicar `S` por `k`.

## v0.1.0 (2016-05-15)
**Adicionados**
* Generalização da equação do calor, de `u_t = u_xx` para `u_t = P(x, y)*u_xx + S(x, y)`.
* Função `func_to_val()` para generalizar as entradas das condições e parâmetros como função, escalar, ou vetor/matriz.

**Removidos**
* Classe base `Base`.

## v0.0.4 (2016-05-14)
**Fixed**
* Com a linha `__metaclass__ = abc.ABCMeta`, a classe `Base` não comporta como deveria, deixando instanciar subclasses mesmo com métodos abstratos não implementados. Solução foi remover essa linha e substituir `object` por `metaclass=abc.ABCMeta`.

## v0.0.3 (2016-05-14)
**Adicionados**
* Nova função `check_conds_type()` que verifica os tipos das condições iniciais e de contornos. Se for do tipo function, aplica os valores de `x` ou `y`.

## v0.0.2 (2016-05-14)
**Modificados**
* Laço com a variável `i` em `explicit()` retirado.

## v0.0.1 (2016-05-14)
**Adicionados**
* Classe `Heat1D` com um método numérico explícito `explicit()` para equação do calor.