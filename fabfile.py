from fabric.api import local


def lint():
    local('isort -rc pdepy tests')
    local('flake8 --max-line-length=119 pdepy tests')


def test():
    lint()
    local('nose2')
