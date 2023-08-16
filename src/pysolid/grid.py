#!/usr/bin/env python3
#######################################################################
# A Python wrapper for solid Earth tides calculation using solid.for.
#   Fortran code is originally written by Dennis Milbert, 2018-06-01.
#   Available at: http://geodesyworld.github.io/SOFTS/solid.htm.
# Author: Zhang Yunjun, Simran Sangha, Sep 2020
# Copyright 2020, by the California Institute of Technology.
#######################################################################
# Recommend usage:
#   import pysolid
#   pysolid.calc_solid_earth_tides_grid()


import os

import numpy as np
from scipy import ndimage


##################################  Earth tides - grid mode  ###################################
def calc_solid_earth_tides_grid(dt_obj, atr, step_size=1e3, display=False, verbose=True):
    """Calculate SET in east/north/up direction for a spatial grid at a given date/time.

    Note that we use step_size to speedup >30 times, by feeding the Fortran code (SET calc and
    text file writing) the coarse grid, then resize the output to the same shape as the original
    input size. This uses the fact that SET varies slowly in space. Comparison w and w/o step_size
    shows a difference in tide_u with max of 5e-8 m, thus negligible.

    Parameters: dt_obj    - datetime.datetime object (with precision up to the second)
                atr       - dict, metadata including the following keys:
                                LENGTH/WIDTTH
                                X/Y_FIRST
                                X/Y_STEP
                step_size - float, grid step feeded into the fortran code in meters
                                to speedup the calculation
                display   - bool, plot the calculated SET
                verbose   - bool, print verbose message
    Returns:    tide_e    - 2D np.ndarray, SET in east  direction in meters
                tide_n    - 2D np.ndarray, SET in north direction in meters
                tide_u    - 2D np.ndarray, SET in up    direction in meters
    Examples:   atr = readfile.read_attribute('geo_velocity.h5')
                tide_e, tide_n, tide_u = calc_solid_earth_tides_grid('20180219', atr)
    """
    try:
        from pysolid.solid import solid_grid
    except ImportError:
        msg = "Cannot import name 'solid' from 'pysolid'!"
        msg += '\n    Maybe solid.for is NOT compiled yet.'
        msg += '\n    Check instruction at: https://github.com/insarlab/PySolid.'
        raise ImportError(msg)

    vprint = print if verbose else lambda *args, **kwargs: None

    # location
    lat0 = float(atr['Y_FIRST'])
    lon0 = float(atr['X_FIRST'])
    lat1 = lat0 + float(atr['Y_STEP']) * int(atr['LENGTH'])
    lon1 = lon0 + float(atr['X_STEP']) * int(atr['WIDTH'])

    vprint('PYSOLID: ----------------------------------------')
    vprint('PYSOLID: datetime: {}'.format(dt_obj.isoformat()))
    vprint('PYSOLID: SNWE: {}'.format((lat1, lat0, lon0, lon1)))

    # step size
    num_step = int(step_size / 108e3 / abs(float(atr['Y_STEP'])))
    num_step = max(1, num_step)
    length = np.rint(int(atr['LENGTH']) / num_step - 1e-4).astype(int)
    width  = np.rint(int(atr['WIDTH'])  / num_step - 1e-4).astype(int)
    lat_step = float(atr['Y_STEP']) * num_step
    lon_step = float(atr['X_STEP']) * num_step
    vprint('SOLID  : calculate solid Earth tides in east/north/up direction')
    vprint('SOLID  : shape: {s}, step size: {la:.4f} by {lo:.4f} deg'.format(
        s=(length, width), la=lat_step, lo=lon_step))

    ## calc solid Earth tides
    tide_e, tide_n, tide_u = solid_grid(dt_obj.year, dt_obj.month, dt_obj.day,
                                        dt_obj.hour, dt_obj.minute, dt_obj.second,
                                        lat0, lat_step, length,
                                        lon0, lon_step, width)

    # resample to the input size
    # via scipy.ndimage.zoom or skimage.transform.resize
    if num_step > 1:
        in_shape = tide_e.shape
        out_shape = (int(atr['LENGTH']), int(atr['WIDTH']))
        vprint('PYSOLID: resize data to the shape of {} using order-1 spline interpolation'.format(out_shape))

        enu = np.stack([tide_e, tide_n, tide_u])
        zoom_factors = [1, *np.divide(out_shape, in_shape)]
        kwargs = dict(order=1, mode="nearest", grid_mode=True)
        tide_e, tide_n, tide_u = ndimage.zoom(enu, zoom_factors, **kwargs)

    # plot
    if display:
        plot_solid_earth_tides_grid(tide_e, tide_n, tide_u, dt_obj)

    return tide_e, tide_n, tide_u


#########################################  Plot  ###############################################
def plot_solid_earth_tides_grid(tide_e, tide_n, tide_u, dt_obj=None,
                                out_fig=None, save=False, display=True):
    """Plot the solid Earth tides in ENU direction."""
    from matplotlib import pyplot as plt, ticker

    # plot
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=[6, 3], sharex=True, sharey=True)
    for ax, data, label in zip(axs.flatten(),
                               [tide_e, tide_n, tide_u],
                               ['East', 'North', 'Up']):
        im = ax.imshow(data*100, cmap='RdBu')
        ax.tick_params(which='both', direction='in', bottom=True, top=True, left=True, right=True)
        fig.colorbar(im, ax=ax, orientation='horizontal', label=label+' [cm]', pad=0.1, ticks=ticker.MaxNLocator(3))
    fig.tight_layout()

    # super title
    if dt_obj is not None:
        axs[1].set_title('solid Earth tides at {}'.format(dt_obj.isoformat()), fontsize=12)

    # output
    if out_fig:
        save = True

    if save:
        if not out_fig:
            out_fig = os.path.abspath('SET_grid.png')
        print('save figure to {}'.format(out_fig))
        fig.savefig(out_fig, bbox_inches='tight', transparent=True, dpi=300)

    if display:
        print('showing...')
        plt.show()
    else:
        plt.close()

    return
