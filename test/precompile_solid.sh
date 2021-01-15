#!/bin/sh
# pre-compile Fortran code solid.for into Python interface for Pthon>=3.6,<=3.9 in macOS/Linux
# This should be run every time when there is a change in solid.for
# Author: Zhang Yunjun, Jan 2021

# run the following in the terminal before executing this script
# conda create --name test --yes
# conda activate test

# make sure to use test env for this purpose to avoid mess up other envs
while true; do
    read -p "Have you run 'conda activate test' yet? [y/n]: " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

# grab the right fortran compiler name for different OS platform
if [[ "$OSTYPE" == "darwin"*  ]]; then
    echo "macOS detected, use gfortran_osx-64 as fortran compiler"
    gfortran="gfortran_osx-64"
elif [[ "$OSTYPE" == "linux-gnu"*  ]]; then
    echo "Linux detected, use gfortran_linux-64 as fortran compiler"
    gfortran="gfortran_linux-64"
fi

# loop for different python version
for version in "3.6" "3.7" "3.8" "3.9"; do

    # install dependencies
    echo "install dependencies with python="$version
    conda install python=$version numpy $gfortran --channel conda-forge --force-reinstall --yes
    
    # compile solid.for
    cd ~/tools/PySolid/pysolid
    f2py -c -m solid solid.for
    echo "finished for python="$version

done


