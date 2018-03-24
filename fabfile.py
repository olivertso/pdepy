from fabric.api import local


def lint():
    local('isort -rc pdepy tests')
    local('flake8 --max-line-length=119 pdepy tests')


def test():
    lint()
    local('nose2')


def coverage(report_type='term-missing'):
    lint()
    local('nose2 --with-coverage --coverage-report {}'.format(report_type))


def distribute():
    coverage()
    local('python setup.py sdist')
    local('python setup.py bdist_wheel')
    local('twine upload dist/*')
