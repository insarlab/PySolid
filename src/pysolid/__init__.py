from importlib.metadata import PackageNotFoundError, version

# get version info
try:
    __version__ = version(__name__)
except PackageNotFoundError:
    print('package is not installed!\n'
          'Please follow the installation instructions in the README.md.\n'
          'Or, to just get the version number, use:\n'
          '   python -m setuptools_scm')


# top-level functions
from .grid import (
    calc_solid_earth_tides_grid,
    plot_solid_earth_tides_grid,
)
from .point import (
    TIDES,
    calc_solid_earth_tides_point,
    plot_solid_earth_tides_point,
    plot_power_spectral_density4tides,
)
from . import py_solid

__all__ = [
    '__version__',
    'calc_solid_earth_tides_grid',
    'plot_solid_earth_tides_grid',
    'TIDES',
    'calc_solid_earth_tides_point',
    'plot_solid_earth_tides_point',
    'plot_power_spectral_density4tides',
    'py_solid',
]
