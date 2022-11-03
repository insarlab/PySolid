# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.

# always prefer setuptools over distutils
import setuptools
from numpy.distutils.core import setup, Extension

setup(
    # fortran extensions to build with numpy.f2py
    ext_modules=[
        Extension(name='pysolid.solid', sources=['src/pysolid/solid.for']),
    ],
)
