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
print('Test solid Earth tides calculation for a time period at a specific location')

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
out_fig = os.path.join(os.path.dirname(__file__), 'test_SET_point.png')
pysolid.plot_solid_earth_tides_point(dt_out, tide_e, tide_n, tide_u, lalo=[lat, lon],
                                     out_fig=out_fig, display=False)

## open the plotted figures
if sys.platform in ['linux']:
    os.system('display {}'.format(out_fig))
elif sys.platform in ['darwin']:
    os.system('open {}'.format(out_fig))
elif sys.platform.startswith('win'):
    os.system(out_fig)
else:
    print('Unknown OS system. Check results in file: {}'.format(out_fig))

