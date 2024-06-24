#!/usr/bin/env python3
# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.


import os
import sys
import datetime as dt

import numpy as np

import pysolid


if __name__ == '__main__':

    # print the file/module path
    print('-'*50)
    print(os.path.abspath(__file__))

    # prepare inputs
    lat, lon = 34.0, -118.0     # Los Angles, CA
    dt_obj0 = dt.datetime(2020, 11,  5, 12, 0, 0)
    dt_obj1 = dt.datetime(2020, 12, 31,  0, 0, 0)

    # reference
    # calculated based on version 0.3.2.post6 on Jun 24, 2024
    # env: macOS with python-3.10, numpy-1.24
    # install: manual compilation via f2py
    dt_out_8000 = np.array(
        [dt.datetime(2020, 11,  5, 12,  0),
         dt.datetime(2020, 11, 11,  1, 20),
         dt.datetime(2020, 11, 16, 14, 40),
         dt.datetime(2020, 11, 22,  4,  0),
         dt.datetime(2020, 11, 27, 17, 20),
         dt.datetime(2020, 12,  3,  6, 40),
         dt.datetime(2020, 12,  8, 20,  0),
         dt.datetime(2020, 12, 14,  9, 20),
         dt.datetime(2020, 12, 19, 22, 40),
         dt.datetime(2020, 12, 25, 12,  0)], dtype=object,
    )
    tide_e_8000 = np.array(
        [-0.02975027,  0.04146837, -0.02690945, -0.00019223,  0.01624152,
          0.0532655 , -0.02140918, -0.05554432,  0.01371739, -0.00516968],
    )
    tide_n_8000 = np.array(
        [-0.01275229, -0.02834036,  0.00886857, -0.03247227, -0.05237735,
         -0.00590791, -0.01990448, -0.01964124, -0.04439581, -0.00410378],
    )
    tide_u_8000 = np.array(
        [ 0.16008235, -0.05721991, -0.15654693, -0.00041214,  0.03041098,
          0.13082217, -0.1006462 ,  0.24870719, -0.02648802, -0.08420228],
    )

    # calculate
    (dt_out,
     tide_e,
     tide_n,
     tide_u) = pysolid.calc_solid_earth_tides_point(lat, lon, dt_obj0, dt_obj1, verbose=False)

    # compare
    assert all(dt_out[::8000] == dt_out_8000)
    assert np.allclose(tide_e[::8000], tide_e_8000)
    assert np.allclose(tide_n[::8000], tide_n_8000)
    assert np.allclose(tide_u[::8000], tide_u_8000)

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
