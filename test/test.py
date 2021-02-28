#!/usr/bin/env python3
# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


import os
import sys
import datetime as dt

# setup path for the package
pysolid_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(pysolid_path)
import pysolid


## pysolid.point
print('\n\nCalculate solid Earth tides for a time period at a specific location')

# prepare inputs
lat, lon = 34.0, -118.0     # Los Angles, CA
dt_obj0 = dt.datetime(2020, 11,  1, 4, 0, 0)
dt_obj1 = dt.datetime(2020, 12, 31, 2, 0, 0)

# calculate
(dt_out,
 tide_e,
 tide_n,
 tide_u) = pysolid.calc_solid_earth_tides_point(lat, lon, dt_obj0, dt_obj1, verbose=False)

# plot
out_fig1 = os.path.join(os.path.dirname(__file__), 'test_SET_point.png')
pysolid.plot_solid_earth_tides_point(dt_out, tide_e, tide_n, tide_u, lalo=[lat, lon],
                                     out_fig=out_fig1, display=False)


## pysolid.grid
print('\n\nCalculate solid Earth tides for a spatial grid at a specific time')

# prepare inputs
dt_obj = dt.datetime(2020, 12, 25, 14, 7, 44)
atr = {
    'LENGTH'  : 400,
    'WIDTH'   : 500,
    'X_FIRST' : -118.2,
    'Y_FIRST' : 33.8,
    'X_STEP'  :  0.000833333,
    'Y_STEP'  : -0.000833333,
}

# calculate
(tide_e,
 tide_n,
 tide_u) = pysolid.calc_solid_earth_tides_grid(dt_obj, atr, verbose=True)

# plot
out_fig2 = os.path.join(os.path.dirname(__file__), 'test_SET_grid.png')
pysolid.plot_solid_earth_tides_grid(tide_e, tide_n, tide_u, dt_obj,
                                    out_fig=out_fig2, display=False)


## open the plotted figures
cmd = 'open'
if sys.platform in ['linux']:
    cmd = 'display'
os.system('{} {}'.format(cmd, out_fig1))
os.system('{} {}'.format(cmd, out_fig2))

