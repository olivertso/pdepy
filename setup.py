from setuptools import setup

setup(
    name = 'pde',
    version = '0.0.3',
    url = 'https://bitbucket.org/olivertso/pde',
    author = 'Oliver Hung Buo Tso',
    packages=['pde'],
    install_requires = [
        'numpy',
        'scipy'
    ]
)