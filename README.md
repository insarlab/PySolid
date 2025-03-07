[![Language](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=flat-square)](https://www.python.org/)
[![CircleCI](https://img.shields.io/circleci/build/github/insarlab/PySolid.svg?logo=circleci&label=tests&style=flat-square)](https://circleci.com/gh/insarlab/PySolid)
[![Conda Download](https://img.shields.io/conda/dn/conda-forge/pysolid?color=green&label=conda%20downloads&style=flat-square)](https://anaconda.org/conda-forge/pysolid)
[![Version](https://img.shields.io/github/v/release/insarlab/PySolid?color=yellow&label=version&style=flat-square)](https://github.com/insarlab/PySolid/releases)
[![License](https://img.shields.io/badge/license-GPLv3+-blue.svg?style=flat-square)](https://github.com/insarlab/PySolid/blob/main/LICENSE)
[![Citation](https://img.shields.io/badge/doi-10.1109%2FTGRS.2022.3168509-blue?style=flat-square)](https://doi.org/10.1109/TGRS.2022.3168509)

## PySolid

The Python based solid Earth tides (PySolid) is a thin Python wrapper of the [`solid.for`](http://geodesyworld.github.io/SOFTS/solid.htm) program (by Dennis Milbert based on [_dehanttideinelMJD.f_](https://iers-conventions.obspm.fr/content/chapter7/software/dehanttideinel/) from V. Dehant, S. Mathews, J. Gipson and C. Bruyninx) to calculate [solid Earth tides](https://en.wikipedia.org/wiki/Earth_tide) in east, north and up directions (section 7.1.1 in the [2010 IERS Conventions](https://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn36.html)). Solid Earth tides introduce large offsets in SAR observations and long spatial wavelength ramps in InSAR observations, as shown in the Sentinel-1 data with regular acquisitions and large swaths ([Yunjun et al., 2022](https://doi.org/10.1109/TGRS.2022.3168509)).

This is research code provided to you "as is" with NO WARRANTIES OF CORRECTNESS. Use at your own risk.

### 1. Install

PySolid is available on the [conda-forge](https://anaconda.org/conda-forge/pysolid) channel and the main archive of the [Debian](https://tracker.debian.org/pkg/pysolid) GNU/Linux OS. The released version can be installed via `conda` as:

```shell
# run "conda update pysolid" to update the installed version
conda install -c conda-forge pysolid
```

or via `apt` (or other package managers) for [Debian-derivative OS](https://wiki.debian.org/Derivatives/Census) users, including [Ubuntu](https://ubuntu.com), as:

```shell
apt install python3-pysolid
```

<details>
<p><summary>Or build from source:</summary></p>

PySolid relies on a few Python modules as described in [requirements.txt](./requirements.txt) and [NumPy's f2py](https://numpy.org/doc/stable/f2py/) to build the Fortran source code. You could use `conda` to install all the dependencies, including the Fortran compiler, or use your own installed Fortran compiler and `pip` to install the rest.

##### a. Download source code

```bash
# run "cd PySolid; git pull" to update to the latest development version
git clone https://github.com/insarlab/PySolid.git
```

##### b. Install dependencies

```bash
# option 1: use conda to install dependencies into an existing, activated environment
conda install -c conda-forge fortran-compiler --file PySolid/requirements.txt --file PySolid/tests/requirements.txt

# option 2: use conda to install dependencies into a new environment, e.g. named "pysolid"
conda create --name pysolid fortran-compiler --file PySolid/requirements.txt --file PySolid/tests/requirements.txt
conda activate pysolid

# option 3: have a Fortran compiler already installed and use pip to install the dependencies
python -m pip install -r PySolid/requirements.txt -r PySolid/tests/requirements.txt
```

##### c. Install PySolid

```bash
# option 1: use pip to install pysolid into the current environment
python -m pip install ./PySolid

# option 2: use pip to install pysolid in develop mode (editable) into the current environment
python -m pip install -e ./PySolid

# option 3: manually compile the Fortran code and setup environment variable
cd PySolid/src/pysolid
f2py -c -m solid solid.for
# Replace <path-to-folder> with proper path to PySolid main folder
export PYTHONPATH=${PYTHONPATH}:<path-to-folder>/PySolid/src
```

##### d. Test the installation

To test the installation, run the following:

```bash
python -c "import pysolid; print(pysolid.__version__)"
python PySolid/tests/grid.py
python PySolid/tests/point.py
```
</details>

### 2. Usage

PySolid could compute solid Earth tides in two modes: **point** and **grid**. Both modes produce displacement in east, north and up directions.

+   **Point mode:** compute 1D tides time-series at a specific point for a given time period
+   **Grid mode:** compute 2D tides grid at a specific time for a given spatial grid

#### 2.1 Point Mode [[notebook](./docs/plot_point_SET.ipynb)]

```python
import datetime as dt
import pysolid

# prepare inputs
lat, lon = 34.0, -118.0                 # point of interest in degree, Los Angles, CA
step_sec = 60 * 5                       # sample spacing in time domain in seconds
dt0 = dt.datetime(2020, 1, 1, 4, 0, 0)  # start date and time
dt1 = dt.datetime(2021, 1, 1, 2, 0, 0)  # end   date and time

# compute SET via pysolid
dt_out, tide_e, tide_n, tide_u = pysolid.calc_solid_earth_tides_point(
    lat, lon, dt0, dt1,
    step_sec=step_sec,
    display=False,
    verbose=False,
)

# plot the power spectral density of SET up component
pysolid.plot_power_spectral_density4tides(tide_u, sample_spacing=step_sec)
```

<p align="left">
  <img width="600" src="./docs/images/set_point_ts.png">
  <img width="600" src="./docs/images/set_point_psd.png">
</p>

#### 2.2 Grid Mode [[notebook](./docs/plot_grid_SET.ipynb)]

```python
import datetime as dt
import numpy as np
import pysolid

# prepare inputs
dt_obj = dt.datetime(2020, 12, 25, 14, 7, 44)
meta = {
    'LENGTH' : 500,                # number of rows
    'WIDTH'  : 450,                # number of columns
    'X_FIRST': -126,               # min longitude in degree (upper left corner of the upper left pixel)
    'Y_FIRST': 43,                 # max laitude   in degree (upper left corner of the upper left pixel)
    'X_STEP' :  0.000925926 * 30,  # output resolution in degree
    'Y_STEP' : -0.000925926 * 30,  # output resolution in degree
}

# compute SET via pysolid
tide_e, tide_n, tide_u = pysolid.calc_solid_earth_tides_grid(
    dt_obj, meta,
    display=False,
    verbose=True,
)

# project SET from ENU to satellite line-of-sight (LOS) direction with positive for motion towards the satellite
# inc_angle : incidence angle of the LOS vector (from ground to radar platform) measured from vertical.
# az_angle  : azimuth   angle of the LOS vector (from ground to radar platform) measured from the north, with anti-clockwirse as positive.
inc_angle = np.deg2rad(34)   # radian, typical value for Sentinel-1
az_angle = np.deg2rad(-102)  # radian, typical value for Sentinel-1 descending track
tide_los = (  tide_e * np.sin(inc_angle) * np.sin(az_angle) * -1
            + tide_n * np.sin(inc_angle) * np.cos(az_angle)
            + tide_u * np.cos(inc_angle))
```

<p align="left">
  <img width="800" src="./docs/images/set_grid.png">
</p>

### 3. Citing this work

+   Yunjun, Z., Fattahi, H., Pi, X., Rosen, P., Simons, M., Agram, P., & Aoki, Y. (2022). Range Geolocation Accuracy of C-/L-band SAR and its Implications for Operational Stack Coregistration. _IEEE Trans. Geosci. Remote Sens., 60_, 5227219. [ [doi](https://doi.org/10.1109/TGRS.2022.3168509) \| [arxiv](https://doi.org/10.31223/X5F641) \| [data](https://doi.org/10.5281/zenodo.6360749) \| [notebook](https://github.com/yunjunz/2022-Geolocation) ]
+   Milbert, D. (2018), "solid: Solid Earth Tide", [Online]. Available: http://geodesyworld.github.io/SOFTS/solid.htm. Accessd on: 2020-09-06.
