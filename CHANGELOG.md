# Change Log

## [Unreleased]

## v0.5.2 (2016.05.27)
**Adicionados**
* Wrappers `laplace()`, `parabolic()` e `wave()` para as classes `Laplace`, `Parabolic` e `Wave`.

## v0.5.1 (2016.05.22)
**Fixed**
* Alguns `print()`.

## v0.5.0 (2016.05.22)
**Adicionados**
* Classe base `TimeDependent` para PDEs dependente do tempo.
* Classe base `SteadyState` para PDEs em estados estacionários.
* Classe `Laplace` para resolver o problema de condições de contorno da equação de Laplace `u_xx + u_yy = 0`.
* Função `_set_parameters()` atualizar os parâmetros para matrizes de tamanho da malha interior de 'u'.
* Função `_mesh_int_grid()` que retorna matrizes 'x' e 'y' conforme o tamanho da malha interior.

**Modificados**
* Trocar `metaclass=abc.ABCMeta` por `abc.ABC`.
* Argumento `conds` não pode mais ser tupla de funções, somente escalar e array_like.
* Função `_check_mthd()`. Trocar `raise Value()` por `sys.exit()`.

**Removidos**
* Funções `_check_arguments()`, `_check_tuple()`, `_check_len()`, `_check_domain()`, `_func_to_val()`.

## v0.4.0 (2016.05.21)
**Adicionados**
* Classe `Base`.
* Classe `Wave` para resolver o problema de condições iniciais e de contorno da equação da onda `u_yy = u_xx` utilizando um método explícito e um implícito.

**Modificados**
* Separação da função `_set_system()` em `_set_mat()` e `_set_vec()`.

## v0.3.0 (2016.05.19)
**Adicionados**
* `_set_𝛉()`, determina o valor de `𝛉`, que difere os métodos explícitos e implícitos.
* `_explicit()`, métodos de diferenças finitas centrais / upwind explícitos.
* `_implicit()`, métodos de diferenças finitas centrais / upwind implícitos.
* `__init__()`, cria o atributo `methods`, uma lista com os métodos numéricos implementados.
* `_check_arguments()`, `_check_tuple()`, `_check_len()` e `_check_mthd()` para verificações dos argumentos de `solve()`.

## v0.2.0 (2016.05.18)
**Adicionados**
* Função `solve()` que prepara os parâmetros para chamar o método especificado conforme a entrada `mthd`.
* Entrada `mthd` para especificar o método.

**Modificados**
* Generalização da classe `Heat1d` que resolve a equação do calor `u_t = P(x, y)*u_xx + S(x, y)` para a classe `Parabolic` que resolve a equação parabólica linear `u_t = p(x, y)*u_xx + q(x, y)*u_x + r(x, y)*u + s(x, y)`.
* Entradas `domain` e `params` do tipo `tuple` para agrupar as entradas do domínio e dos parâmetros. `tuple` em vez de `list` para garantir que as entradas não sejam modificadas depois da execução do programa.

**Removidos**
* Função `check_conds_type()`.

**Fixed**
* Criar a função `_test()` para testes, pois funções dentro da calsse podem acessar variáveis no `if __name__ == '__main__':` caso não estejam definidas localmente.

## v0.1.1 (2016.05.15)
**Fixed**
* Em `Heat1D().exp_central()`, multiplicar `S` por `k`.

## v0.1.0 (2016.05.15)
**Adicionados**
* Generalização da equação do calor, de `u_t = u_xx` para `u_t = P(x, y)*u_xx + S(x, y)`.
* Função `func_to_val()` para generalizar as entradas das condições e parâmetros como função, escalar, ou vetor/matriz.

**Removidos**
* Classe base `Base`.

## v0.0.4 (2016.05.14)
**Fixed**
* Com a linha `__metaclass__ = abc.ABCMeta`, a classe `Base` não comporta como deveria, deixando instanciar subclasses mesmo com métodos abstratos não implementados. Solução foi remover essa linha e substituir `object` por `metaclass=abc.ABCMeta`.

## v0.0.3 (2016.05.14)
**Adicionados**
* Nova função `check_conds_type()` que verifica os tipos das condições iniciais e de contornos. Se for do tipo function, aplica os valores de `x` ou `y`.

## v0.0.2 (2016.05.14)
**Modificados**
* Laço com a variável `i` em `explicit()` retirado.

## v0.0.1 (2016.05.14)
**Adicionados**
* Classe `Heat1D` com um método numérico explícito `explicit()` para equação do calor.