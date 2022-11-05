# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.

# always prefer setuptools over distutils
import setuptools
from numpy.distutils.core import setup, Extension

setup(
    ## add the following redundant setup for setuptools<60, the latter is required for numpy.distutils
    name='pysolid',

    # package discovery
    packages=setuptools.find_packages("src"),  # include all packages under src
    package_dir={"": "src"},                   # tell distutils packages are under src

    # data files
    include_package_data=True,
    package_data={
        "pysolid": ["solid.for"],
    },

    ## fortran extensions to build with numpy.f2py
    ext_modules=[
        Extension(name='pysolid.solid', sources=['src/pysolid/solid.for']),
    ],
)
