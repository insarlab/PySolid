[![Language](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-v0.1.2-green.svg)](https://github.com/insarlab/PySolid/releases)
[![License](https://img.shields.io/badge/license-GPLv3-yellow.svg)](https://github.com/insarlab/PySolid/blob/main/LICENSE)
[![render](https://img.shields.io/badge/render-nbviewer-orange.svg)](https://nbviewer.jupyter.org/github/insarlab/PySolid/tree/main/docs)

## PySolid

The Python based solid Earth tides (PySolid) is a thin Python wrapper of the [`solid.for`](http://geodesyworld.github.io/SOFTS/solid.htm) program (by Dennis Milbert based on [_dehanttideinelMJD.f_](https://iers-conventions.obspm.fr/content/chapter7/software/dehanttideinel/) from V. Dehant, S. Mathews, J. Gipson and C. Bruyninx) to calculate [solid Earth tides](https://en.wikipedia.org/wiki/Earth_tide) in east/north/up direction (section 7.1.1 in the [2010 IERS Conventions](https://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn36.html)). Solid Earth tides introduces very long spatial wavelength range components in SAR/InSAR observations, as shown in the Sentinel-1 data with regular acquisitions and large swaths (Fattahi et al., 2020).

This is research code provided to you "as is" with NO WARRANTIES OF CORRECTNESS. Use at your own risk.

### 1. Install

PySolid relies on a few Python modules as described in [requirements.txt](./requirements.txt) and compilation of the Fortran code.

#### a. Use `pip` to install the pre-compiled version

We maintain a few pre-compiled version of the Fortran code, so that one could install PySolid via pip as below, without the fortran compiler and manual compilation. However, this works for recent numpy versions on macOS and Linux only.

```bash
# use "pip install --upgrade" to update to the latest version
pip install git+https://github.com/insarlab/PySolid.git
```

#### b. Use `conda` to compile from source

Below is example of using conda to compile from source:

```bash
# download source code
cd ~/tools
git clone https://github.com/insarlab/PySolid.git

# install dependencies via conda
conda install -c conda-forge --file PySolid/requirements.txt

# compile the Fortran code into a Python interface using f2py to generate the C extension files, e.g.:
# solid.cpython-37m-darwin.so           for macOS
# solid.cpython-37m-x86_64-linux-gnu.so for Linux
cd ~/tools/PySolid/pysolid
f2py -c -m solid solid.for
```

Set the following environment variable (e.g. in **_~/.bash_profile_** for _bash_ users or **_~/.cshrc_** for _csh/tcsh_ users). 

```bash
export PYTHONPATH=${PYTHONPATH}:~/tools/PySolid
```

#### Test

To test the installation, run the following:

```bash
python -c "import pysolid; print(pysolid.__version__)"
~/tools/PySolid/test/test.py
```

### 2. Example Usage

PySolid could compute solid Earth tides in two modes: **point** and **grid**. Both modes produce displacement in east, north and up direction.

+   **Point mode:** compute 1D tides time-series at a specific point for a given time period
+   **Grid mode:** compute 2D tides grid at a specific time for a given spatial grid

#### 2.1 Point Mode [[nbviewer](https://nbviewer.jupyter.org/github/insarlab/PySolid/blob/main/docs/plot_point_SET.ipynb)]

```python
import datetime as dt
import pysolid

# prepare inputs
lat, lon = 34.0, -118.0                 # point of interest in degree, Los Angles, CA
step_sec = 60 * 5                       # sample spacing in time domain in seconds
dt0 = dt.datetime(2020, 1, 1, 4, 0, 0)  # start date and time
dt1 = dt.datetime(2021, 1, 1, 2, 0, 0)  # end   date and time

# compute SET via pysolid
(dt_out,
 tide_e,
 tide_n,
 tide_u) = pysolid.calc_solid_earth_tides_point(lat, lon, dt0, dt1,
                                                step_sec=step_sec,
                                                display=False,
                                                verbose=False)

# plot the power spectral density of SET up component
pysolid.plot_power_spectral_density4tides(tide_u, sample_spacing=step_sec)
```

<p align="left">
  <img width="600" src="https://yunjunzhang.files.wordpress.com/2021/01/set_ts_up-1.png">
  <img width="600" src="https://yunjunzhang.files.wordpress.com/2021/01/set_psd-1.png">
</p>

#### 2.2 Grid Mode [[nbviewer](https://nbviewer.jupyter.org/github/insarlab/PySolid/blob/main/docs/plot_grid_SET.ipynb)]

```python
import datetime as dt
import numpy as np
import pysolid

# prepare inputs
dt_obj = dt.datetime(2020, 12, 25, 14, 7, 44)
atr = {
    'LENGTH' : 500,                # number of rows
    'WIDTH'  : 450,                # number of columns
    'X_FIRST': -126,               # min longitude in degree (upper left corner of the upper left pixel)
    'Y_FIRST': 43,                 # max laitude   in degree (upper left corner of the upper left pixel)
    'X_STEP' :  0.000925926 * 30,  # output resolution in degree
    'Y_STEP' : -0.000925926 * 30,  # output resolution in degree
}

# compute SET via pysolid
(tide_e,
 tide_n,
 tide_u) = pysolid.calc_solid_earth_tides_grid(dt_obj, atr,
                                               display=False,
                                               verbose=True)

# project SET from ENU to radar line-of-sight (LOS) direction with positive for motion towards satellite
inc_angle  =   34.0 / 180. * np.pi  # radian, typical value for Sentinel-1
head_angle = -168.0 / 180. * np.pi  # radian, typical value for Sentinel-1 desc track
tide_los = (  tide_e * np.sin(inc_angle) * np.cos(head_angle) * -1
            + tide_n * np.sin(inc_angle) * np.sin(head_angle)
            + tide_u * np.cos(inc_angle))
```

<p align="left">
  <img width="800" src="https://yunjunzhang.files.wordpress.com/2021/01/set_grid-3.png">
</p>

### 3. References

+   Milbert, D. (2018), solid: Solid Earth Tide, Available: http://geodesyworld.github.io/SOFTS/solid.htm, Accessd on: 2020-09-06.
+   Fattahi, H., Yunjun, Z., Pi, X., Agram, P.S., Rosen, P., and Aoki, Y. (2020), Absolute geolocation of SAR Big-Data: The first step for operational InSAR time-series analysis, _AGU Fall Meeting 2020_, 1-17 Dec 2020.
+   Petit, G., and Luzum, B. (2010), [IERS Conventions (2010) (IERS Technical Note No. 36)](https://iers-conventions.obspm.fr/conventions_material.php) 179 pp., _International Earth Rotation And Reference Systems Service (IERS)_, Frankfurt, Germany. [[Code](https://iers-conventions.obspm.fr/chapter7.php)].
