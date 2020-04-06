"""
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from os import path

from setuptools import setup


def read(filename):
    with open(path.join(path.dirname(__file__), filename), encoding="utf-8") as f:
        return f.read()


setup(
    name="pdepy",
    version="1.0.3",
    description="A Finite-Difference PDE solver.",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    url="https://github.com/olivertso/pdepy",
    author="Oliver Hung Buo Tso",
    author_email="olivertsor@gmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords="partial-differential-equations finite-difference-method",
    packages=["pdepy"],
    install_requires=read("requirements.in").splitlines(),
    python_requires=">=3.6",
)
