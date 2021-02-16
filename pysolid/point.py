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
import collections
import datetime as dt
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt, ticker, dates as mdates

try:
    from .solid import solid_point
except ImportError:
    msg = "Cannot import name 'solid' from 'pysolid'!"
    msg += '\n    Maybe solid.for is NOT compiled yet.'
    msg += '\n    Check instruction at: https://github.com/insarlab/PySolid.'
    raise ImportError(msg)


## Tidal constituents
# https://en.wikipedia.org/wiki/Theory_of_tides#Tidal_constituents
Tag = collections.namedtuple('Tag', 'species symbol period speed doodson_num noaa_order')
TIDES = (
    # Semi-diurnal
    Tag('Principal lunar semidiurnal'              , r'$M_2$'      , 12.421, 28.984, 255.555, 1 ),
    Tag('Principal solar semidiurnal'              , r'$S_2$'      , 12.000, 30.000, 273.555, 2 ),
    Tag('Larger lunar elliptic semidiurnal'        , r'$N_2$'      , 12.658, 28.440, 245.655, 3 ),
    Tag('Larger lunar evectional'                  , r'$v_2$'      , 12.626, 28.513, 247.455, 11),
    Tag('Variational'                              , r'$\mu_2$'    , 12.872, 27.968, 237.555, 13),
    Tag('Lunar elliptical semidiurnal second-order', '2"N'+r'$_2$' , 12.905, 27.895, 235.755, 14),
    Tag('Smaller lunar evectional'                 , r'$\lambda_2$', 12.222, 29.456, 263.655, 16),
    Tag('Larger solar elliptic'                    , r'$T_2$'      , 12.016, 29.959, 272.555, 27),
    Tag('Smaller solar elliptic'                   , r'$R_2$'      , 11.984, 30.041, 274.555, 28),
    Tag('Shallow water semidiurnal'                , r'$2SM_2$'    , 11.607, 31.016, 291.555, 31),
    Tag('Smaller lunar elliptic semidiurnal'       , r'$L_2$'      , 12.192, 29.528, 265.455, 33),
    Tag('Lunisolar semidiurnal'                    , r'$K_2$'      , 11.967, 30.082, 275.555, 35),

    # Diurnal
    Tag('Lunar diurnal'                  , r'$K_1$' , 23.934, 15.041, 165.555, 4 ),
    Tag('Lunar diurnal'                  , r'$O_1$' , 25.819, 13.943, 145.555, 6 ),
    Tag('Lunar diurnal'                  , r'$OO_1$', 22.306, 16.139, 185.555, 15),
    Tag('Solar diurnal'                  , r'$S_1$' , 24.000, 15.000, 164.555, 17),
    Tag('Smaller lunar elliptic diurnal' , r'$M_1$' , 24.841, 14.492, 155.555, 18),
    Tag('Smaller lunar elliptic diurnal' , r'$J_1$' , 23.098, 15.585, 175.455, 19),
    Tag('Larger lunar evectional diurnal', r'$\rho$', 26.723, 13.472, 137.455, 25),
    Tag('Larger lunar elliptic diurnal'  , r'$Q_1$' , 26.868, 13.399, 135.655, 26),
    Tag('Larger elliptic diurnal'        , r'$2Q_1$', 28.006, 12.854, 125.755, 29),
    Tag('Solar diurnal'                  , r'$P_1$' , 24.066, 14.959, 163.555, 30),

    # Long period
    Tag('Lunar monthly'                  , r'$M_m$'   ,  661.311, 0.544, 65.455, 20),  # period  27.555 days
    Tag('Solar semiannual'               , r'$S_{sa}$', 4383.076, 0.082, 57.555, 21),  # period 182.628 days
    Tag('Solar annual'                   , r'$S_a$'   , 8766.153, 0.041, 56.555, 22),  # period 365.256 days
    Tag('Lunisolar synodic fortnightly'  , r'$MS_f$'  ,  354.367, 1.016, 73.555, 23),  # period  14.765 days
    Tag('Lunisolar fortnightly'          , r'$M_f$'   ,  327.860, 1.098, 75.555, 24),  # period  13.661 days

    # Short period
    Tag('Shallow water overtides of principal lunar', r'$M_4$'      , 6.210,  57.968, 455.555, 5 ),
    Tag('Shallow water overtides of principal lunar', r'$M_6$'      , 4.140,  86.952, 655.555, 7 ),
    Tag('Shallow water terdiurnal'                  , r'$MK_3$'     , 8.177,  44.025, 365.555, 8 ),
    Tag('Shallow water overtides of principal solar', r'$S_4$'      , 6.000,  60.000, 491.555, 9 ),
    Tag('Shallow water quarter diurnal'             , r'$MN_4$'     , 6.269,  57.424, 445.655, 10),
    Tag('Shallow water overtides of principal solar', r'$S_6$'      , 4.000,  90.000, np.NaN , 12),
    Tag('Lunar terdiurnal'                          , r'$M_3$'      , 8.280,  43.476, 355.555, 32),
    Tag('Shallow water terdiurnal'                  , '2"MK'+r'$_3$', 8.386,  42.927, 345.555, 34),
    Tag('Shallow water eighth diurnal'              , r'$M_8$'      , 3.105, 115.936, 855.555, 36),
    Tag('Shallow water quarter diurnal'             , r'$MS_4$'     , 6.103,  58.984, 473.555, 37),
)


##################################  Earth tides - point mode  ##################################
def calc_solid_earth_tides_point(lat, lon, dt0, dt1, step_sec=60, display=False, verbose=True):
    """Calculate SET in east/north/up direction for the given time period at the given point (lat/lon).

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
    for one day at the given point (lat/lon).

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
    for _ in range(2):
        solid_point(lat, lon, t.year, t.month, t.day, step_sec)

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
def plot_solid_earth_tides_point(dt_out, tide_e, tide_n, tide_u, lalo=None,
                                 out_fig=None, save=False, display=True):
    """Plot the solid Earth tides at one point."""
    # plot
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=[6, 4], sharex=True)
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

    # output
    if out_fig:
        save = True

    if save:
        if not out_fig:
            out_fig = os.path.abspath('SET_point.png')
        print('save figure to {}'.format(out_fig))
        fig.savefig(out_fig, bbox_inches='tight', transparent=True, dpi=300)

    if display:
        print('showing...')
        plt.show()
    else:
        plt.close()

    return


def plot_power_spectral_density4tides(tide_ts, sample_spacing, out_fig=None, fig_dpi=300, min_psd=1500):
    """Plot the power spectral density (PSD) of tides time-series.
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
        add_tidal_constituents(ax, period, psd, min_psd=min_psd)
    axs[0].annotate('semi-diurnal', xy=(0.05,0.85), xycoords='axes fraction')
    axs[1].annotate('diurnal',      xy=(0.05,0.85), xycoords='axes fraction')

    # output
    if out_fig:
        print('save figure to file:', os.path.abspath(out_fig))
        fig.savefig(out_fig, bbox_inches='tight', transparent=True, dpi=fig_dpi)
    plt.show()

    return


def add_tidal_constituents(ax, period, psd, min_psd=1500, verbose=False):
    """Mark tidal constituents covered in the axes."""
    pmin, pmax = ax.get_xlim()
    for tide in TIDES:
        if pmin <= tide.period <= pmax:
            tide_psd = psd[np.argmin(np.abs(period - tide.period))]
            if tide_psd >= min_psd:
                ymax = tide_psd / ax.get_ylim()[1]
                ax.axvline(x=tide.period, ymax=ymax, color='k', ls='--', lw=1)
                ax.annotate(tide.symbol, xy=(tide.period, tide_psd))
                if verbose:
                    print('tide: speices={}, symbol={}, period={} hours, psd={} m^2/Hz'.format(
                        tide.species, tide.symbol, tide.period, tide_psd))
    return
