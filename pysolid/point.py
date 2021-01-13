#!/usr/bin/env python3
#######################################################################
# A Python wrapper for solid Earth tides calculation using solid.for.
#   Fortran code is originally written by Dennis Milbert, 2018-06-01.
#   Available at: http://geodesyworld.github.io/SOFTS/solid.htm.
# Author: Zhang Yunjun, Jan 2021
# Copyright 2020, by the California Institute of Technology.
#######################################################################
# Recommend usage:
#   import pysolid
#   pysolid.calc_solid_earth_tides_point()


import os
import datetime as dt
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt, ticker, dates as mdates

try:
    from . import solid
except ImportError:
    msg = "Cannot import name 'solid' from 'pysolid'!"
    msg += '\n    Maybe solid.for is NOT compiled yet.'
    msg += '\n    Check instruction at: https://github.com/insarlab/PySolid.'
    raise ImportError(msg)


# Tidal constituents
# https://en.wikipedia.org/wiki/Theory_of_tides#Tidal_constituents
TIDAL_CONSTITUENTS = {
    # semi-diurnal
    r'$M_2$' : 12.421,  # principal lunar       semi-diurnal
    r'$S_2$' : 12.000,  # principal solar       semi-diurnal
    r'$N_2$' : 12.658,  # larger lunar elliptic semi-diurnal
    r'$K_2$' : 11.967,  # lunisolar             semi-diurnal
    # diurnal
    r'$K_1$' : 23.934,  # lunar                 diurnal
    r'$O_1$' : 25.819,  # lunar                 diurnal
    r'$P_1$' : 24.066,  # solar                 diurnal
    r'$Q_1$' : 26.868,  # larger lunar elliptic diurnal
    # long period
    r'$M_f$' : 13.661 * 24,  # lunisolar fornightly
    r'$M_m$' : 27.555 * 24,  # lunar monthly
}



##################################  Earth tides - point mode  ##################################
def calc_solid_earth_tides_point(lat, lon, dt0, dt1, step_sec=60, display=False, verbose=True):
    """Calculate solid Earth tides (SET) in east/north/up direction
    for the given time period at the given point (lat/lon)

    Parameters: lat/lon  - float32, latitude/longitude of the point of interest
                dt0/1    - datetime.datetime object, start/end date and time
                step_sec - int16, time step in seconds
                display  - bool, plot the calculated SET
                verbose  - bool, print verbose message
    Returns:    dt_out   - 1D np.ndarray in dt.datetime objects
                tide_e   - 1D np.ndarray in float32, SET in east  direction in meters
                tide_n   - 1D np.ndarray in float32, SET in north direction in meters
                tide_u   - 1D np.ndarray in float32, SET in up    direction in meters
    Examples:   dt0 = dt.datetime(2020,11,1,4,0,0)
                dt1 = dt.datetime(2020,12,31,2,0,0)
                (dt_out,
                 tide_e,
                 tide_n,
                 tide_u) = calc_solid_earth_tides_point(34.0, -118.0, dt0, dt1)
    """

    print('PYSOLID: calculate solid Earth tides in east/north/up direction')
    print('PYSOLID: lot/lon: {}/{} degree'.format(lat, lon))
    print('PYSOLID: start UTC: {}'.format(dt0.isoformat()))
    print('PYSOLID: end   UTC: {}'.format(dt1.isoformat()))
    print('PYSOLID: time step: {} seconds'.format(step_sec))

    dt_out = []
    tide_e = []
    tide_n = []
    tide_u = []

    ndays = (dt1.date() - dt0.date()).days + 1
    for i in range(ndays):
        di = dt0.date() + dt.timedelta(days=i)
        if verbose:
            print('SOLID  : {} {}/{} ...'.format(di.isoformat(), i+1, ndays))

        # calc tide_u/n/u for the whole day
        (dt_outi,
         tide_ei,
         tide_ni,
         tide_ui) = calc_solid_earth_tides_point_per_day(lat, lon,
                                                         date_str=di.strftime('%Y%m%d'),
                                                         step_sec=int(step_sec))

        # flag to mark the first/last datetime
        if i == 0:
            flag = dt_outi >= dt0
        elif i == ndays - 1:
            flag = dt_outi <= dt1
        else:
            flag = np.ones(dt_outi.size, dtype=np.bool_)

        # update
        dt_out += dt_outi[flag].tolist()
        tide_e += tide_ei[flag].tolist()
        tide_n += tide_ni[flag].tolist()
        tide_u += tide_ui[flag].tolist()

    # list --> np.ndarray for output
    dt_out = np.array(dt_out)
    tide_e = np.array(tide_e)
    tide_n = np.array(tide_n)
    tide_u = np.array(tide_u)

    # plot
    if display:
        plot_solid_earth_tides_point(dt_out, tide_e, tide_n, tide_u, lalo=[lat, lon])

    return dt_out, tide_e, tide_n, tide_u


def calc_solid_earth_tides_point_per_day(lat, lon, date_str, step_sec=60):
    """Calculate solid Earth tides (SET) in east/north/up direction
    for one day at the given point (lat/lon)

    Parameters: lat/lon  - float32, latitude/longitude of the point of interest
                date_str - str, date in YYYYMMDD
                step_sec - int16, time step in seconds
    Returns:    dt_out   - 1D np.ndarray in dt.datetime objects
                tide_e   - 1D np.ndarray in float32, SET in east  direction in meters
                tide_n   - 1D np.ndarray in float32, SET in north direction in meters
                tide_u   - 1D np.ndarray in float32, SET in up    direction in meters
    Examples:   (dt_out,
                 tide_e,
                 tide_n,
                 tide_u) = calc_solid_earth_tides_point_per_day(34.0, -118.0, '20180219')
    """

    ## calc solid Earth tides and write to text file
    txt_file = os.path.abspath('solid.txt')
    if os.path.isfile(txt_file):
        os.remove(txt_file)

    # Run twice to circumvent fortran bug which cuts off last file in loop - Simran, Jun 2020
    t = dt.datetime.strptime(date_str, '%Y%m%d')
    for i in range(2):
        solid.solid_point(lat, lon, t.year, t.month, t.day, step_sec)

    ## read data from text file
    num_row = int(24 * 60 * 60 / step_sec)
    fc = np.loadtxt(txt_file,
                    dtype=float,
                    delimiter=',',
                    skiprows=0,
                    max_rows=num_row)

    tide_e = fc[:, 1].flatten()
    tide_n = fc[:, 2].flatten()
    tide_u = fc[:, 3].flatten()

    secs   = fc[:, 0].flatten()
    dt_out = [t + dt.timedelta(seconds=sec) for sec in secs]
    dt_out = np.array(dt_out)

    # remove the temporary text file
    os.remove(txt_file)

    return dt_out, tide_e, tide_n, tide_u


#########################################  Plot  ###############################################
def plot_solid_earth_tides_point(dt_out, tide_e, tide_n, tide_u, lalo=None):
    """Plot the solid Earth tides at one point."""

    # plot
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=[12, 6], sharex=True)
    for ax, data, label in zip(axs.flatten(),
                               [tide_e, tide_n, tide_u],
                               ['East [cm]', 'North [cm]', 'Up [cm]']):
        ax.plot(dt_out, data*100)
        ax.set_ylabel(label, fontsize=12)

    # axis format
    for ax in axs:
        ax.tick_params(which='both', direction='out', bottom=True, top=False, left=True, right=True)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_minor_locator(mdates.DayLocator())

    if lalo:
        axs[0].set_title('solid Earth tides at (N{}, E{})'.format(lalo[0], lalo[1]), fontsize=12)
    fig.tight_layout()

    plt.show()
    return


def plot_power_spectral_density4tides(tide_ts, sample_spacing, out_fig=None, fig_dpi=300):
    """Plot the power spectral density (PSD) of tides time-series
    Note: for accurate PSD analysis, a long time-series, e.g. one year, is recommended.
    """

    ## calc PSD
    freq, psd = signal.periodogram(tide_ts, fs=1/sample_spacing, scaling='density')
    # get rid of zero in the first element
    psd = psd[1:]
    freq = freq[1:]
    period = 1./3600./freq   # period (hour)

    ## plot
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=[8,3], sharey=True)
    for ax in axs:
        ax.plot(period, psd, '.', ms=16, mfc='none', mew=2)

    # axis format
    for ax in axs:
        ax.tick_params(which='both', direction='out', bottom=True, top=True, left=True, right=True)
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.set_xlabel('Period [hour]')
    axs[0].set_xlim(11.3, 13.2)
    axs[1].set_xlim(22.0, 28.0)
    ax = axs[0]
    ax.set_ylabel('Power Spectral Density\n'+r'[$m^2/Hz$]')
    ax.set_ylim(0, ymax=axs[0].get_ylim()[1] * 1.1)
    #ax.set_ylim(1e-1,5e6);  plt.yscale('log')
    #ax.yaxis.set_major_locator(ticker.FixedLocator([0,50e3,100e3,150e3]))
    #ax.set_yticklabels(['0','50k','100k','150k'])
    fig.tight_layout()

    # Tidal constituents
    for ax in axs:
        pmin, pmax = ax.get_xlim()
        for tide_name, tide_period in TIDAL_CONSTITUENTS.items():
            if pmin <= tide_period <= pmax:
                ind = np.argmin(np.abs(period - tide_period))
                ymax = psd[ind] / ax.get_ylim()[1]
                ax.axvline(x=tide_period, ymax=ymax, color='k', ls='--', lw=1)
                ax.annotate(tide_name, xy=(tide_period, psd[ind]))
    axs[0].annotate('semi-diurnal', xy=(0.05,0.85), xycoords='axes fraction')
    axs[1].annotate('diurnal',      xy=(0.05,0.85), xycoords='axes fraction')

    # output
    if out_fig:
        print('save figure to file:', os.path.abspath(out_fig))
        fig.savefig(out_fig, bbox_inches='tight', transparent=True, dpi=fig_dpi)
    plt.show()

    return

