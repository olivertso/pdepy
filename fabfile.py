from fabric.api import local


def lint():
    local('isort -rc pde tests')
    local('flake8 --max-line-length=119 pde tests')


def test():
    lint()
    local('nose2')
