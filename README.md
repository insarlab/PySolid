[![Language](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPLv3-yellow.svg)](https://github.com/insarlab/MintPy/blob/main/LICENSE)

## Solid Earth tides

Solid Earth tides (SET) introduces very long spatial wavelength range components in SAR/InSAR. We use the [`solid.for`](http://geodesyworld.github.io/SOFTS/solid.htm) program (by Dennis Milbert based on [_dehanttideinelMJD.f_](https://iers-conventions.obspm.fr/content/chapter7/software/dehanttideinel/) from V. Dehant, S. Mathews, J. Gipson and C. Bruyninx) to calculate solid Earth tides in east/north/up direction (section 7.1.2 in the [2003 IERS Conventions](https://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn32.html)) via a thin python wrapper `pysolid` module.

### 1. Install



#### 1.1 Use pre-compiled version

Use pip to install the pre-compiled version as below. This works for macOS/Linux only.

```bash
pip install git+https://github.com/insarlab/PySolid.git
```

#### 1.2 Build from source



```bash
# download source code
cd ~/tools
git clone https://github.com/insarlab/PySolid.git

# install dependencies
# including the Fortran compiler from conda: gfortran_osx/linux-64
conda install gfortran_osx-64 --file PySolid/requirements.txt

# compile Fortran code into a Python interface using f2py to generate:
# solid.cpython-37m-darwin.so           for macOS
# solid.cpython-37m-x86_64-linux-gnu.so for Linux
cd ~/tools/PySolid/pysolid
f2py -c -m solid solid.for
```

Set the following environment variables in your source file (e.g. **_~/.bash_profile_** for _bash_ users or **_~/.cshrc_** for _csh/tcsh_ users).

```bash
export PYTHONPATH=${PYTHONPATH}:~/tools/PySolid
```

Run the following to test the installation:

```bash
python -c "import pysolid; print(pysolid.__version__)"
```

### 2. References

+ Milbert, D., SOLID EARTH TIDE, http://geodesyworld.github.io/SOFTS/solid.htm, Accessd 2020 September 6.
+ Fattahi, H., Z. Yunjun, X. Pi, P. S. Agram, P. Rosen, and Y. Aoki (2020), Absolute geolocation of SAR Big-Data: The first step for operational InSAR time-series analysis, _AGU Fall Meeting 2020_, 1-17 Dec 2020.
+ McCarthy, D. D., and G. Petit (2004), [IERS conventions (2003) (IERS Technical Note No. 32)](https://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn32.html), 127 pp, _International Earth Rotation And Reference Systems Service (IERS)_, Frankfurt, Germany.
+ Petit, G., and B. Luzum (2010), [IERS Conventions (2010) (IERS Technical Note No. 36)](https://iers-conventions.obspm.fr/conventions_material.php) 179 pp., _International Earth Rotation And Reference Systems Service (IERS)_, Frankfurt, Germany. [[Code](https://iers-conventions.obspm.fr/chapter7.php)].
