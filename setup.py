# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.

# always prefer setuptools over distutils
import setuptools
from numpy.distutils.core import setup, Extension

# read the contents of README file
def readme():
    with open("README.md") as f:
        return f.read()

setup(
    ## add the following redundant setup for setuptools<60, the latter is required for numpy.distutils
    name="pysolid",
    description="A Python wrapper for solid to compute solid Earth tides",
    url="https://github.com/insarlab/PySolid",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Zhang Yunjun, Dennis Milbert",
    author_email="yunjunz@outlook.com",
    license="GPL-3.0-or-later",
    license_files=("LICENSE",),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    keywords="solid Eartth tides, deformation, geodesy, geophysics",

    project_urls={
        "Bug Reports": "https://github.com/insarlab/PySolid/issues",
        "Source": "https://github.com/insarlab/PySolid",
    },

    # dependencies
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
    ],

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
        Extension(name="pysolid.solid", sources=["src/pysolid/solid.for"])
    ],
)
