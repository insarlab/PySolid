# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.
from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension(name='pysolid.solid', sources=['src/pysolid/solid.for']),
    ],
)
