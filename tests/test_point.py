"""Test suite for point-based solid earth tide calculations."""

import datetime as dt
import numpy as np
import pytest
from pysolid import py_solid
import pysolid


@pytest.mark.parametrize(
    "module",
    [
        pytest.param(py_solid, id="python_impl"),
        pytest.param(pysolid, id="fortran_impl"),
    ],
)
def test_point_calculation(module):
    """Test point-based solid earth tide calculations."""
    # Test inputs
    lat, lon = 34.0, -118.0
    dt_obj0 = dt.datetime(2020, 11, 5, 12, 0, 0)
    dt_obj1 = dt.datetime(2020, 12, 31, 0, 0, 0)

    # Reference outputs
    ref_dates = np.array(
        [
            dt.datetime(2020, 11, 5, 12, 0),
            dt.datetime(2020, 11, 11, 1, 20),
            dt.datetime(2020, 11, 16, 14, 40),
            dt.datetime(2020, 11, 22, 4, 0),
            dt.datetime(2020, 11, 27, 17, 20),
            dt.datetime(2020, 12, 3, 6, 40),
            dt.datetime(2020, 12, 8, 20, 0),
            dt.datetime(2020, 12, 14, 9, 20),
            dt.datetime(2020, 12, 19, 22, 40),
            dt.datetime(2020, 12, 25, 12, 0),
        ],
        dtype=object,
    )

    ref_tide_e = np.array(
        [
            -0.02975027,
            0.04146837,
            -0.02690945,
            -0.00019223,
            0.01624152,
            0.0532655,
            -0.02140918,
            -0.05554432,
            0.01371739,
            -0.00516968,
        ]
    )

    ref_tide_n = np.array(
        [
            -0.01275229,
            -0.02834036,
            0.00886857,
            -0.03247227,
            -0.05237735,
            -0.00590791,
            -0.01990448,
            -0.01964124,
            -0.04439581,
            -0.00410378,
        ]
    )

    ref_tide_u = np.array(
        [
            0.16008235,
            -0.05721991,
            -0.15654693,
            -0.00041214,
            0.03041098,
            0.13082217,
            -0.1006462,
            0.24870719,
            -0.02648802,
            -0.08420228,
        ]
    )

    # Run calculation
    dt_out, tide_e, tide_n, tide_u = module.calc_solid_earth_tides_point(
        lat, lon, dt_obj0, dt_obj1, verbose=False
    )

    # Check results
    assert all(d1 == d2 for (d1, d2) in zip(dt_out[::8000], ref_dates))
    np.testing.assert_array_almost_equal(tide_e[::8000], ref_tide_e)
    np.testing.assert_array_almost_equal(tide_n[::8000], ref_tide_n)
    np.testing.assert_array_almost_equal(tide_u[::8000], ref_tide_u)


@pytest.mark.parametrize(
    "module",
    [
        pytest.param(py_solid, id="python_impl"),
        pytest.param(pysolid, id="fortran_impl"),
    ],
)
def test_point_input_validation(module):
    """Test input validation for point calculations."""
    with pytest.raises(ValueError):
        # Invalid latitude
        module.calc_solid_earth_tides_point(
            91.0,
            -118.0,
            dt.datetime.now(),
            dt.datetime.now() + dt.timedelta(days=1),
            verbose=False,
        )

    with pytest.raises(ValueError):
        # invalid longitude
        module.calc_solid_earth_tides_point(
            34.0,
            -500.0,
            dt.datetime.now(),
            dt.datetime.now() + dt.timedelta(days=1),
            verbose=False,
        )
