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
    dt_obj = dt.datetime(2020, 12, 25, 14, 7, 44)
    atr = {
        'LENGTH'  : 400,
        'WIDTH'   : 500,
        'X_FIRST' : -118.2,
        'Y_FIRST' : 33.8,
        'X_STEP'  :  0.000833333,
        'Y_STEP'  : -0.000833333,
    }

    # reference
    # calculated based on version 0.3.2.post6 on Jun 24, 2024
    # env: macOS with python-3.10, numpy-1.24
    # install: manual compilation via f2py
    tide_e_80_100 = np.array(
        [[0.01628786, 0.01630887, 0.01633078, 0.01635247, 0.01637394],
         [0.01633248, 0.01635348, 0.01637538, 0.01639706, 0.01641851],
         [0.01638009, 0.01640107, 0.01642296, 0.01644462, 0.01646606],
         [0.01642767, 0.01644864, 0.01647052, 0.01649217, 0.01651359],
         [0.01647523, 0.01649619, 0.01651805, 0.01653968, 0.01656109]],
    )
    tide_n_80_100 = np.array(
        [[-0.02406203, -0.02412341, -0.02418807, -0.02425273, -0.0243174 ],
         [-0.02407558, -0.02413699, -0.02420168, -0.02426637, -0.02433107],
         [-0.02408992, -0.02415136, -0.02421608, -0.02428081, -0.02434554],
         [-0.02410413, -0.0241656 , -0.02423036, -0.02429511, -0.02435988],
         [-0.02411821, -0.02417972, -0.0242445 , -0.02430929, -0.02437408]],
    )
    tide_u_80_100 = np.array(
        [[-0.05548462, -0.05533455, -0.05517631, -0.05501789, -0.05485928],
         [-0.05529561, -0.0551451 , -0.05498639, -0.0548275 , -0.05466843],
         [-0.05509374, -0.05494276, -0.05478355, -0.05462417, -0.05446461],
         [-0.05489176, -0.05474031, -0.05458061, -0.05442073, -0.05426067],
         [-0.05468968, -0.05453776, -0.05437757, -0.05421719, -0.05405664]],
    )

    # calculate
    (tide_e,
     tide_n,
     tide_u) = pysolid.calc_solid_earth_tides_grid(dt_obj, atr, verbose=True)

    # compare
    assert np.allclose(tide_e[::80, ::100], tide_e_80_100)
    assert np.allclose(tide_n[::80, ::100], tide_n_80_100)
    assert np.allclose(tide_u[::80, ::100], tide_u_80_100)

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
