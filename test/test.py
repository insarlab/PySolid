#!/usr/bin/env python3
# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


import datetime as dt
import pysolid



## pysolid.point
print('\n\nCalculate solid Earth tides for a time period at a specific location')

# prepare inputs
lat, lon = 34.0, -118.0 # Los Angles, CA
dt0 = dt.datetime(2020,11,1,4,0,0)
dt1 = dt.datetime(2020,12,31,2,0,0)

# call
(dt_out,
 tide_e,
 tide_n,
 tide_u) = pysolid.calc_solid_earth_tides_point(lat, lon, dt0, dt1,
                                                display=True,
                                                verbose=False)



## pysolid.grid
print('\n\nCalculate solid Earth tides for a spatial grid at a specific time')

# inputs
date_str = '20201225'
atr = {}
atr['LENGTH'] = 400
atr['WIDTH'] = 500
atr['X_FIRST'] = -118.2
atr['Y_FIRST'] = 33.8
atr['X_STEP'] =  0.000833333
atr['Y_STEP'] = -0.000833333
atr['CENTER_LINE_UTC'] = 50864.0

# call
(tide_e,
 tide_n,
 tide_u) = pysolid.calc_solid_earth_tides_grid(date_str, atr,
                                               display=True,
                                               verbose=True)

