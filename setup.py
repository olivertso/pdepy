"""
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pdepy',
    version='1.0.2',
    description='A Finite-Difference PDE solver.',
    long_description=long_description,
    url='https://github.com/olivertso/pdepy',
    author='Oliver Hung Buo Tso',
    author_email='olivertsor@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development'
    ],
    keywords='partial-differential-equations finite-difference-method',
    packages=['pdepy'],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.14.2',
        'scipy>=1.0.0'
    ]
)
