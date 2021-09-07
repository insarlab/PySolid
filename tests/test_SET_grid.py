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


## pysolid.grid
print('Test solid Earth tides calculation for a spatial grid at a specific time')

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
out_fig = os.path.join(os.path.dirname(__file__), 'test_SET_grid.png')
pysolid.plot_solid_earth_tides_grid(tide_e, tide_n, tide_u, dt_obj,
                                    out_fig=out_fig, display=False)


## open the plotted figures
cmd = 'open'
if sys.platform in ['linux']:
    cmd = 'display'
os.system('{} {}'.format(cmd, out_fig))

