# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


# always prefer setuptools over distutils
from setuptools import setup, find_packages

setup(
    name='pysolid',
    version='0.1.2',
    description="A Python wrapper for solid to compute solid Earth tides",
    url="https://github.com/insarlab/PySolid",
    author="Zhang Yunjun, Dennis Milbert",
    author_email="yunjunzgeo@gmail.com",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="solid Eartth tides, deformation, geodesy, geophysics",

    # package discovery
    packages=find_packages(),

    # dependencies
    python_requires=">=3.6",
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'scikit-image',
    ],

    # data files
    include_package_data=True,
    package_data={
        "pysolid": [
            "solid.for",
            "solid.cpython*.so",
        ],
    },

    project_urls={
        "Bug Reports": "https://github.com/insarlab/PySolid/issues",
        "Source": "https://github.com/insarlab/PySolid",
    },
)
