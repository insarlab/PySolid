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
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pic'))
    os.makedirs(out_dir, exist_ok=True)

    out_fig = os.path.join(out_dir, 'grid.png')
    pysolid.plot_solid_earth_tides_grid(
        tide_e, tide_n, tide_u, dt_obj,
        out_fig=out_fig,
        display=False)

    # open the plotted figures
    if sys.platform in ['linux']:
        os.system(f'display {out_fig}')
    elif sys.platform in ['darwin']:
        os.system(f'open {out_fig}')
    elif sys.platform.startswith('win'):
        os.system(out_fig)
    else:
        print(f'Unknown OS system ({sys.platform}). Check results in file: {out_fig}.')
