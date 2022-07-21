#!/usr/bin/env python3
# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


import os
import sys
import datetime as dt

import pysolid


if __name__ == '__main__':

    # print the file/module path
    print('-'*50)
    print(os.path.abspath(__file__))

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
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pic'))
    os.makedirs(out_dir, exist_ok=True)

    out_fig = os.path.join(out_dir, 'point.png')
    pysolid.plot_solid_earth_tides_point(
        dt_out, tide_e, tide_n, tide_u,
        lalo=[lat, lon],
        out_fig=out_fig,
        display=False)

    # open the saved figure
    if sys.platform in ['linux']:
        os.system(f'display {out_fig}')
    elif sys.platform in ['darwin']:
        os.system(f'open {out_fig}')
    elif sys.platform.startswith('win'):
        os.system(out_fig)
    else:
        print(f'Unknown OS system ({sys.platform}). Check results in file: {out_fig}.')
