# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.

# always prefer setuptools over distutils
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from numpy import f2py
import os
import subprocess
import sys

# read the contents of README file
def readme():
    with open("README.md") as f:
        return f.read()

class f2py_build(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        # Reuse setuptools build_ext logic for output location and name
        build_dir, fname = os.path.split(super().get_ext_fullpath(ext.name))
        module = fname.split(".")[0]

        # Compile a Fortran module using f2py
        c = [sys.executable, "-m", "numpy.f2py", "-c"]
        # Specify module name and source file paths
        c += ["-m", module] + [os.path.abspath(x) for x in ext.sources]
        # Use meson backend (enforces python 3.12+ behavior, not needed)
        #c += ["--backend", "meson"]

        # No way to specify the output location,
        # so we have to run with CWD as the destination directory
        subprocess.run(c, cwd=build_dir)

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

    cmdclass=dict(build_ext=f2py_build),
)
