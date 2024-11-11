from __future__ import annotations
from dataclasses import dataclass
import datetime
import numpy as np
import numpy.typing as npt


# GRS 80
ellp_a = 6378137.0
ellp_e2 = 6.69438002290341574957e-03

# Degrees to radians
rad = 180.0 / np.pi
deg2rad = 0.017453292519943295769

# http://maia.usno.navy.mil/ser7/tai-utc.dat
leap_seconds_min = 10.0
leap_seconds_limit = 60854.0  # 2025 JUN 28
leap_second_epochs = np.array([
    41317,  # 1972 JAN  1 =JD 2441317.5  TAI-UTC=  10.0s
    41499,  # 1972 JUL  1 =JD 2441499.5  TAI-UTC=  11.0s
    41683,  # 1973 JAN  1 =JD 2441683.5  TAI-UTC=  12.0s
    42048,  # 1974 JAN  1 =JD 2442048.5  TAI-UTC=  13.0s
    42413,  # 1975 JAN  1 =JD 2442413.5  TAI-UTC=  14.0s
    42778,  # 1976 JAN  1 =JD 2442778.5  TAI-UTC=  15.0s
    43144,  # 1977 JAN  1 =JD 2443144.5  TAI-UTC=  16.0s
    43509,  # 1978 JAN  1 =JD 2443509.5  TAI-UTC=  17.0s
    43874,  # 1979 JAN  1 =JD 2443874.5  TAI-UTC=  18.0s
    44239,  # 1980 JAN  1 =JD 2444239.5  TAI-UTC=  19.0s
    44786,  # 1981 JUL  1 =JD 2444786.5  TAI-UTC=  20.0s
    45151,  # 1982 JUL  1 =JD 2445151.5  TAI-UTC=  21.0s
    45516,  # 1983 JUL  1 =JD 2445516.5  TAI-UTC=  22.0s
    46247,  # 1985 JUL  1 =JD 2446247.5  TAI-UTC=  23.0s
    47161,  # 1988 JAN  1 =JD 2447161.5  TAI-UTC=  24.0s
    47892,  # 1990 JAN  1 =JD 2447892.5  TAI-UTC=  25.0s
    48357,  # 1991 JAN  1 =JD 2448257.5  TAI-UTC=  26.0s
    48804,  # 1992 JUL  1 =JD 2448804.5  TAI-UTC=  27.0s
    49169,  # 1993 JUL  1 =JD 2449169.5  TAI-UTC=  28.0s
    49534,  # 1994 JUL  1 =JD 2449534.5  TAI-UTC=  29.0s
    50083,  # 1996 JAN  1 =JD 2450083.5  TAI-UTC=  30.0s
    50630,  # 1997 JUL  1 =JD 2450630.5  TAI-UTC=  31.0s
    51179,  # 1999 JAN  1 =JD 2451179.5  TAI-UTC=  32.0s
    53736,  # 2006 JAN  1 =JD 2453736.5  TAI-UTC=  33.0s
    54832,  # 2009 JAN  1 =JD 2454832.5  TAI-UTC=  34.0s
    56109,  # 2012 JUL  1 =JD 2456109.5  TAI-UTC=  35.0s
    57204,  # 2015 JUL  1 =JD 2457204.5  TAI-UTC=  36.0s
    57754,  # 2017 JAN  1 =JD 2457754.5  TAI-UTC=  37.0s
], dtype=int)


# Fixed data
datdi_step2lon = np.array([
    [0, 0, 0, 1, 0, 0.47, 0.23, 0.16, 0.07],
    [0, 2, 0, 0, 0, -0.20, -0.12, -0.11, -0.05],
    [1, 0, -1, 0, 0, -0.11, -0.08, -0.09, -0.04],
    [2, 0, 0, 0, 0, -0.13, -0.11, -0.15, -0.07],
    [2, 0, 0, 1, 0, -0.05, -0.05, -0.06, -0.03]
])

datdi_step2diu = np.array([
    [-3., 0., 2., 0., 0., -0.01, -0.01, 0.0, 0.0],
    [-3., 2., 0., 0., 0., -0.01, -0.01, 0.0, 0.0],
    [-2., 0., 1., -1., 0., -0.02, -0.01, 0.0, 0.0],
    [-2., 0., 1., 0., 0., -0.08, 0.00, 0.01, 0.01],
    [-2., 2., -1., 0., 0., -0.02, -0.01, 0.0, 0.0],
    [-1., 0., 0., -1., 0., -0.10, 0.00, 0.00, 0.00],
    [-1., 0., 0., 0., 0., -0.51, 0.00, -0.02, 0.03],
    [-1., 2., 0., 0., 0., 0.01, 0.0, 0.0, 0.0],
    [0., -2., 1., 0., 0., 0.01, 0.0, 0.0, 0.0],
    [0., 0., -1., 0., 0., 0.02, 0.01, 0.0, 0.0],
    [0., 0., 1., 0., 0., 0.06, 0.00, 0.00, 0.00],
    [0., 0., 1., 1., 0., 0.01, 0.0, 0.0, 0.0],
    [0., 2., -1., 0., 0., 0.01, 0.0, 0.0, 0.0],
    [1., -3., 0., 0., 1., -0.06, 0.00, 0.00, 0.00],
    [1., -2., 0., 1., 0., 0.01, 0.0, 0.0, 0.0],
    [1., -2., 0., 0., 0., -1.23, -0.07, 0.06, 0.01],
    [1., -1., 0., 0., -1., 0.02, 0.0, 0.0, 0.0],
    [1., -1., 0., 0., 1., 0.04, 0.0, 0.0, 0.0],
    [1., 0., 0., -1., 0., -0.22, 0.01, 0.01, 0.00],
    [1., 0., 0., 0., 0., 12.00, -0.78, -0.67, -0.03],
    [1., 0., 0., 1., 0., 1.73, -0.12, -0.10, 0.00],
    [1., 0., 0., 2., 0., -0.04, 0.0, 0.0, 0.0],
    [1., 1., 0., 0., -1., -0.50, -0.01, 0.03, 0.00],
    [1., 1., 0., 0., 1., 0.01, 0.0, 0.0, 0.0],
    [1., 1., 0., 1., -1., -0.01, 0.0, 0.0, 0.0],
    [1., 2., -2., 0., 0., -0.01, 0.0, 0.0, 0.0],
    [1., 2., 0., 0., 0., -0.11, 0.01, 0.01, 0.00],
    [2., -2., 1., 0., 0., -0.01, 0.0, 0.0, 0.0],
    [2., 0., -1., 0., 0., -0.02, 0.02, 0.0, 0.01],
    [3., 0., 0., 0., 0., 0.0, 0.01, 0.0, 0.01],
    [3., 0., 0., 1., 0., 0.0, 0.01, 0.0, 0.0]
])


@np.vectorize
def gps2tai(tgps: float) -> float:
    """Convert GPS time (sec) to TAI (sec)"""
    return tgps + 19.0


@np.vectorize
def tai2ttt(ttai: float) -> float:
    """Convert TAI (sec) to Terrestrial Time (sec)"""
    return ttai + 32.184


@np.vectorize
def gps2ttt(tgps: float) -> float:
    """Convert GPS time (sec) to Terrestrial Time (sec)"""
    ttai = gps2tai(tgps)
    return tai2ttt(ttai)


def tai_utcday(dutc: npt.ArrayLike) -> npt.ArrayLike:
    """Get TAI-UTC for given UTC (day)"""
    ind = np.searchsorted(leap_second_epochs, dutc, side="right") - 1

    # Return limits of table for dates before and after the table span
    return ind.clip(0, leap_second_epochs.size - 1) + leap_seconds_min


def utc2tai(day: npt.ArrayLike,
            tutc: npt.ArrayLike) -> tuple[npt.ArrayLike, npt.ArrayLike]:
    """Convert UTC (sec) to TAI (sec) on a given day"""

    adjustment = np.floor(tutc / 86400.0).astype(int)
    adj_day = day + adjustment
    adj_tutc = tutc - adjustment * 86400

    return adj_day, adj_tutc + tai_utcday(adj_day)


def utc2ttt(day: npt.ArrayLike,
            tutc: npt.ArrayLike) -> tuple[npt.ArrayLike, npt.ArrayLike]:
    """Convert UTC (sec) to Terrestrial Time (sec)"""
    adj_day, ttai = utc2tai(day, tutc)
    return adj_day, tai2ttt(ttai)


@dataclass
class CivDate:
    iyr: int
    imo: int
    idy: int
    ihr: int
    imn: int
    sec: float

    @property
    def secs_of_day(self) -> float:
        return (
            self.ihr * 3600.0 + self.imn * 60.0 + self.sec
        )

    def civmjd(self) -> ModJulDate:
        """Convert Civil Date to Julian Date"""

        y = self.iyr
        m = self.imo

        if m <= 2:
            y = y - 1
            m = m + 12

        it1 = int(365.25 * y)
        it2 = int(30.6001 * (m + 1))
        mjd = int(it1 + it2 + self.idy - 679019)
        fmjd = self.secs_of_day / 86400.0
        return ModJulDate(mjd, fmjd)

    def civjts(self, mjd0: int) -> float:
        """Convert Civil Date to time in seconds past mjd0 epoch"""
        jul = self.civmjd()
        tsec = (jul.mjd - mjd0) * 86400.0 + self.secs_of_day
        return tsec


@dataclass
class ModJulDate:
    mjd: int
    fmjd: float

    @property
    def rjd(self) -> float:
        return self.mjd + self.fmjd + 2400000.5

    def mjdciv(self) -> CivDate:
        """Convert Modified Julian Date to Civil Date"""

        ia = int(self.rjd + 0.5)
        ib = ia + 1537
        ic = int((ib - 122.1)/365.25)
        idd = int(365.25 * ic)
        ie = int((ib - idd) / 30.6001)

        # the fractional part of a julian day is fractional mjd + 0.5
        # therefore, fractional part of julian day + 0.5 is fractional mjd
        it1 = int(ie * 30.6001)
        idy = int(ib - idd - it1 + self.fmjd)
        it2 = int(ie / 14.0)
        imo = int(ie - 1 - 12 * it2)
        it3 = int((7 + imo) / 10.0)
        iyr = int(ic - 4715 - it3)

        tmp = self.fmjd * 24.0
        ihr = int(tmp)
        tmp = (tmp - ihr) * 60.0
        imn = int(tmp)
        sec = (tmp - imn) * 60.0
        return CivDate(iyr, imo, idy, ihr, imn, sec)

    def getghar(self) -> float:
        """Convert to Greenwich hour angle in radians"""
        # need UTC to get sidereal time
        # ("astronomy on the personal computer", 4th ed)
        # (pg.43, montenbruck & pfleger, springer, 2005)

        tsecutc = self.fmjd * 86400.0
        fmjdutc = tsecutc / 86400.0

        # d = MJD - 51544.5d0
        # footnote
        # days since J2000
        d = (self.mjd - 51544) + (fmjdutc - 0.50)

        # greenwich hour angle for J2000  (12:00:00 on 1 Jan 2000)
        # ghad = 100.46061837504d0 + 360.9856473662862d0*d
        # eq. 2.85 (+digits)
        # corrn.   (+digits)
        ghad = 280.460618375040 + 360.98564736628620 * d

        # normalize to 0-360 and convert to radians

        ii = int(ghad / 360.0)
        ghar = (ghad - ii * 360.0) / rad

        pi2 = 2 * np.pi
        ghar -= np.floor(ghar / pi2) * pi2

        return ghar


def jtsciv(tsec: float, mjd0: int) -> CivDate:
    """Convert time in seconds past mjd0 epoch into Civil Date"""

    mjd = int(mjd0 + tsec / 86400.0)
    fmjd = np.remainder(tsec, 86400.0) / 86400.0
    jul = ModJulDate(mjd, fmjd)
    return jul.mjdciv()


@dataclass
class XYZ:
    x: float = 0.
    y: float = 0.
    z: float = 0.

    def enorm8(self) -> float:
        return np.linalg.norm([self.x, self.y, self.z])

    def rot3(self, theta: float) -> XYZ:
        """Rotate coordinate axes about 3 axis by angle of theta radians"""
        s = np.sin(theta)
        c = np.cos(theta)
        uvw = XYZ()
        uvw.x = c * self.x + s * self.y
        uvw.y = c * self.y - s * self.x
        uvw.z = self.z
        return uvw

    def rot1(self, theta: float) -> XYZ:
        """Rotate coordinate axes about 1 axis by angle of theta radians"""
        s = np.sin(theta)
        c = np.cos(theta)
        uvw = XYZ()
        uvw.x = self.x
        uvw.y = c * self.y + s * self.z
        uvw.z = c * self.z - s * self.y
        return uvw

    def rge(self, llh: LLH) -> XYZ:
        """Cartesian xyz to Geocentric cartesian at given lat, lon"""

        sb = np.sin(llh.lat)
        cb = np.cos(llh.lat)
        sl = np.sin(llh.lon)
        cl = np.cos(llh.lon)
        uvw = XYZ()

        uvw.x = -sb * cl * self.x - sb * sl * self.y + cb * self.z
        uvw.y = -sl * self.x + cl * self.y
        uvw.z = cb * cl * self.x + cb * sl * self.y + sb * self.z
        return uvw

    def lhsaaz(self) -> XYZ:
        """Convert local horizontal coordinates to range, azimuth, vertical"""

        s2 = self.x * self.x + self.y * self.y
        r2 = s2 + self.z * self.z

        s = np.sqrt(s2)

        aaz = XYZ()
        aaz.x = np.sqrt(r2)
        aaz.y = np.arctan2(self.y, self.x)
        aaz.z = np.arctan2(self.z, s)
        return aaz


@dataclass
class LLH:
    lat: float
    lon: float
    hte: float

    def geoxyz(self) -> XYZ:
        """Geodetic lat, long, hte to xyz"""

        sla = np.sin(self.lat)
        cla = np.cos(self.lat)
        w2 = 1.0 - ellp_e2 * sla * sla
        w = np.sqrt(w2)
        en = ellp_a / w

        xyz = XYZ()

        xyz.x = (en + self.hte) * cla * np.cos(self.lon)
        xyz.y = (en + self.hte) * cla * np.sin(self.lon)
        xyz.z = (en * (1.0 - ellp_e2) + self.hte) * sla
        return xyz


def sunxyz(jul: ModJulDate) -> XYZ:
    """Get low precision geocentric coordinates for sun (ECEF)"""
    # mean elements for year 2000, sun ecliptic orbit wrt. Earth
    # obliquity of the J2000 ecliptic
    obe = 23.43929111 / rad
    sobe = np.sin(obe)
    cobe = np.cos(obe)
    # RAAN + arg.peri.  (deg.)
    opod = 282.9400

    # use TT for solar ephemerides
    tsecutc = jul.fmjd * 86400.0
    _, tsectt = utc2ttt(jul.mjd, tsecutc)
    fmjdtt = tsectt / 86400.0

    # julian centuries since 1.5 january 2000 (J2000)
    # (note: also low precision use of mjd --> tjd)
    tjdtt = jul.mjd + fmjdtt + 2400000.5
    t = (tjdtt - 2451545.0) / 36525.0
    emdeg = 357.5256 + 35999.049 * t
    em = emdeg / rad
    em2 = em + em

    # series expansions in mean anomaly, em   (eq. 3.43, p.71)
    # m.
    r = (149.619 - 2.499 * np.cos(em) - 0.021 * np.cos(em2)) * 1.0e9
    slond = opod + emdeg + (6892.0 * np.sin(em) + 72.0 * np.sin(em2)) / 3600.0

    # precession of equinox wrt. J2000   (p.71)
    # degrees
    slond = slond + 1.3972 * t

    # position vector of sun (mean equinox & ecliptic of J2000) (EME2000, ICRF)
    # plus long. advance due to precession -- eq. above

    # radians
    slon = slond / rad
    sslon = np.sin(slon)
    cslon = np.cos(slon)

    # meters  eq. 3.46, p.71
    rs1 = r * cslon
    rs2 = r * sslon * cobe
    rs3 = r * sslon * sobe

    # convert position vector of sun to ECEF  (ignore polar motion/LOD)
    # 2.3.1,p.33
    # eq. 2.89, p.37
    ghar = jul.getghar()
    return XYZ(rs1, rs2, rs3).rot3(ghar)


def moonxyz(jul: ModJulDate) -> XYZ:
    """get low-precision, geocentric coordinates for moon (ECEF)"""
    # 1."satellite orbits: models, methods, applications"
    # montenbruck & gill(2000)
    # section 3.3.2, pg. 72-73
    # 2."astronomy on the personal computer, 4th ed."
    # montenbruck & pfleger (2005)
    # section 3.2, pg. 38-39  routine MiniMoon

    # use TT for lunar ephemerides
    tsecutc = jul.fmjd * 86400.0
    _, tsectt = utc2ttt(jul.mjd, tsecutc)
    fmjdtt = tsectt / 86400.0

    # julian centuries since 1.5 january 2000 (J2000)
    # (note: also low precision use of mjd --> tjd)

    # Julian Date, TT
    # julian centuries, TT
    tjdtt = jul.mjd + fmjdtt + 2400000.5
    t = (tjdtt - 2451545.0) / 36525.0

    # el0 -- mean longitude of Moon (deg)
    # el  -- mean anomaly of Moon (deg)
    # elp -- mean anomaly of Sun  (deg)
    # f   -- mean angular distance of Moon from ascending node (deg)
    # d   -- difference between mean longitudes of Sun and Moon (deg)

    # equations 3.47, p.72

    el0 = 218.31617 + 481267.88088 * t - 1.3972 * t
    el = 134.96292 + 477198.86753 * t
    elp = 357.52543 + 35999.04944 * t
    f = 93.27283 + 483202.01873 * t
    d = 297.85027 + 445267.11135 * t
    rad = 180.0 / np.pi

    # longitude w.r.t. equinox and ecliptic of year 2000

    # eq 3.48, p.72
    selond = el0 \
        + 22640.0 / 3600.0 * np.sin((el) / rad) \
        + 769.0 / 3600.0 * np.sin((el + el) / rad) \
        - 4586.0 / 3600.0 * np.sin((el - d - d) / rad) \
        + 2370.0 / 3600.0 * np.sin((d + d) / rad) \
        - 668.0 / 3600.0 * np.sin((elp) / rad) \
        - 412.0 / 3600.0 * np.sin((f + f) / rad) \
        - 212.0 / 3600.0 * np.sin((el + el - d - d) / rad) \
        - 206.0 / 3600.0 * np.sin((el + elp - d - d) / rad) \
        + 192.0 / 3600.0 * np.sin((el + d + d) / rad) \
        - 165.0 / 3600.0 * np.sin((elp - d - d) / rad) \
        + 148.0 / 3600.0 * np.sin((el - elp) / rad) \
        - 125.0 / 3600.0 * np.sin((d)/rad) \
        - 110.0 / 3600.0 * np.sin((el + elp) / rad) \
        - 55.0 / 3600.0 * np.sin((f + f - d - d)/rad)

    # latitude w.r.t. equinox and ecliptic of year 2000
    # temporary term
    q = 412.0 / 3600.0 * np.sin((f + f) / rad) +\
        541.0 / 3600.0 * np.sin((elp) / rad)

    # eq 3.49, p.72
    selatd = 18520.0 / 3600.0 * np.sin((f + selond - el0 + q)/rad) \
        - 526.0 / 3600.0 * np.sin((f - d - d)/rad) \
        + 44.0 / 3600.0 * np.sin((el + f - d - d) / rad) \
        - 31.0 / 3600.0 * np.sin((-el + f - d - d) / rad) \
        - 25.0 / 3600.0 * np.sin((-el - el + f) / rad) \
        - 23.0 / 3600.0 * np.sin((elp + f - d - d) / rad) \
        + 21.0 / 3600.0 * np.sin((-el + f) / rad) \
        + 11.0 / 3600.0 * np.sin((-elp + f - d - d) / rad)

    # distance from Earth center to Moon (m)

    # eq 3.50, p.72
    rse = 385000.0 * 1000.0 \
        - 20905.0 * 1000.0 * np.cos((el)/rad) \
        - 3699.0 * 1000.0 * np.cos((d + d - el)/rad) \
        - 2956.0 * 1000.0 * np.cos((d + d) / rad) \
        - 570.0 * 1000.0 * np.cos((el + el) / rad) \
        + 246.0 * 1000.0 * np.cos((el + el - d - d) / rad) \
        - 205.0 * 1000.0 * np.cos((elp - d - d) / rad) \
        - 171.0 * 1000.0 * np.cos((el + d + d) / rad) \
        - 152.0 * 1000.0 * np.cos((el + elp - d - d) / rad)

    # convert spherical ecliptic coordinates to equatorial cartesian
    # precession of equinox wrt. J2000   (p.71)

    # degrees
    selond = selond + 1.3972 * t

    # position vector of moon
    # (mean equinox & ecliptic of J2000) (EME2000, ICRF)
    # (plus long. advance due to precession -- eq. above)

    # obliquity of the J2000 ecliptic
    oblir = 23.43929111 / rad

    sselat = np.sin(selatd / rad)
    cselat = np.cos(selatd / rad)
    sselon = np.sin(selond / rad)
    cselon = np.cos(selond / rad)

    # meters  !*** eq. 3.51, p.72
    t1 = rse * cselon * cselat
    t2 = rse * sselon * cselat
    t3 = rse * sselat

    # eq. 3.51, p.72
    rm = XYZ(t1, t2, t3).rot1(-oblir)

    # convert position vector of moon to ECEF  (ignore polar motion/LOD)

    # *** sec 2.3.1,p.33
    # *** eq. 2.89, p.37
    ghar = jul.getghar()
    return rm.rot3(ghar)


def sprod(x: XYZ, y: XYZ) -> tuple[float, float, float]:
    r1 = x.enorm8()
    r2 = y.enorm8()
    scal = x.x * y.x + x.y * y.y + x.z * y.z
    return scal, r1, r2


def st1isem(
    xsta: XYZ,
    xsun: XYZ,
    xmon: XYZ,
    fac2sun: float,
    fac2mon: float
) -> XYZ:
    """
    out-of-phase corrections induced by
    mantle inelasticity in the diurnal band
    """
    dhi = -0.0022
    dli = -0.0007

    rsta = xsta.enorm8()
    sinphi = xsta.z / rsta
    cosphi = np.sqrt(xsta.x ** 2 + xsta.y ** 2) / rsta
    sinla = xsta.y / cosphi / rsta
    cosla = xsta.x / cosphi / rsta
    costwola = cosla ** 2 - sinla ** 2
    sintwola = 2.0 * cosla * sinla
    rmon = xmon.enorm8()
    rsun = xsun.enorm8()
    drsun = -3.0 / 4.0 * dhi * cosphi ** 2 * fac2sun \
        * ((xsun.x ** 2 - xsun.y**2) * sintwola
            - 2.0 * xsun.x * xsun.y * costwola) / rsun ** 2
    drmon = -3.0 / 4.0 * dhi * cosphi ** 2 * fac2mon \
        * ((xmon.x ** 2 - xmon.y ** 2) * sintwola
            - 2.0 * xmon.x * xmon.y * costwola) / rmon ** 2
    dnsun = 1.50 * dli * sinphi * cosphi * fac2sun \
        * ((xsun.x ** 2 - xsun.y ** 2) * sintwola
            - 2.0 * xsun.x * xsun.y * costwola) / rsun ** 2
    dnmon = 1.50 * dli * sinphi * cosphi * fac2mon \
        * ((xmon.x ** 2 - xmon.y ** 2) * sintwola
            - 2.0 * xmon.x * xmon.y * costwola) / rmon ** 2
    desun = -3.0 / 2.0 * dli * cosphi * fac2sun \
        * ((xsun.x ** 2 - xsun.y ** 2) * costwola
            + 2.0 * xsun.x * xsun.y * sintwola) / rsun ** 2
    demon = -3.0 / 2.0 * dli * cosphi * fac2mon \
        * ((xmon.x ** 2 - xmon.y ** 2) * costwola
            + 2.0 * xmon.x * xmon.y * sintwola) / rmon ** 2
    dr = drsun + drmon
    dn = dnsun + dnmon
    de = desun + demon
    return XYZ(
        dr * cosla * cosphi - de * sinla - dn * sinphi * cosla,
        dr * sinla * cosphi + de * cosla - dn * sinphi * sinla,
        dr * sinphi + dn * cosphi
    )


def st1idiu(
    xsta: XYZ,
    xsun: XYZ,
    xmon: XYZ,
    fac2sun: float,
    fac2mon: float
) -> XYZ:
    """
    out-of-phase corrections induced by
    mantle inelasticity in the diurnal band
    """
    dhi = -0.0025
    dli = -0.0007

    rsta = xsta.enorm8()
    sinphi = xsta.z / rsta
    cosphi = np.sqrt(xsta.x ** 2 + xsta.y ** 2) / rsta
    sinla = xsta.y / cosphi / rsta
    cosla = xsta.x / cosphi / rsta
    cos2phi = cosphi ** 2 - sinphi ** 2
    rmon = xmon.enorm8()
    rsun = xsun.enorm8()
    drsun = -3.0 * dhi * sinphi * cosphi * fac2sun * xsun.z \
        * (xsun.x * sinla - xsun.y * cosla) / rsun ** 2
    drmon = -3.0 * dhi * sinphi * cosphi * fac2mon * xmon.z \
        * (xmon.x * sinla - xmon.y * cosla) / rmon ** 2
    dnsun = -3.0 * dli * cos2phi * fac2sun * xsun.z \
        * (xsun.x * sinla - xsun.y * cosla) / rsun ** 2
    dnmon = -3.0 * dli * cos2phi * fac2mon * xmon.z \
        * (xmon.x * sinla - xmon.y * cosla) / rmon ** 2
    desun = -3.0 * dli * sinphi * fac2sun * xsun.z \
        * (xsun.x * cosla + xsun.y * sinla) / rsun ** 2
    demon = -3.0 * dli * sinphi * fac2mon * xmon.z \
        * (xmon.x * cosla + xmon.y * sinla) / rmon ** 2
    dr = drsun + drmon
    dn = dnsun + dnmon
    de = desun + demon
    return XYZ(
        dr * cosla * cosphi - de * sinla - dn * sinphi * cosla,
        dr * sinla * cosphi + de * cosla - dn * sinphi * sinla,
        dr * sinphi + dn * cosphi
    )


def step2lon(xsta: XYZ, fhr: float, t: float) -> XYZ:
    s = 218.31664563 + 481267.88194 * t - 0.0014663889 * t * t \
        + 0.00000185139 * t ** 3
    pr = 1.396971278 * t + 0.000308889 * t * t + 0.000000021 * t ** 3 \
        + 0.000000007 * t ** 4
    s = s + pr
    h = 280.46645 + 36000.7697489 * t + 0.00030322222 * t * t \
        + 0.000000020 * t ** 3 - 0.00000000654 * t ** 4
    p = 83.35324312 + 4069.01363525 * t - 0.01032172222 * t * t \
        - 0.0000124991 * t ** 3 + 0.00000005263 * t ** 4
    zns = 234.95544499 + 1934.13626197 * t - 0.00207561111 * t * t \
        - 0.00000213944 * t ** 3 + 0.00000001650 * t ** 4
    ps = 282.93734098 + 1.71945766667 * t + 0.00045688889 * t * t \
        - 0.00000001778 * t ** 3 - 0.00000000334 * t ** 4
    rsta = xsta.enorm8()
    sinphi = xsta.z / rsta
    cosphi = np.sqrt(xsta.x ** 2 + xsta.y ** 2) / rsta
    cosla = xsta.x / cosphi / rsta
    sinla = xsta.y / cosphi / rsta

    # reduce angles to between 0 and 360
    s = np.remainder(s, 360.0)
    # tau=dmod(tau,360.d0)       !*** tau not used here--09jul28
    h = np.remainder(h, 360.0)
    p = np.remainder(p, 360.0)
    zns = np.remainder(zns, 360.0)
    ps = np.remainder(ps, 360.0)

    dr_tot = 0.0
    dn_tot = 0.0
    xcorsta = XYZ()
    datdi = datdi_step2lon.T

    # ***             1 2 3 4   5   6      7      8      9
    # columns are s,h,p,N',ps, dR(ip),dT(ip),dR(op),dT(op)

    for jj in range(5):
        thetaf = (datdi[0, jj] * s + datdi[1, jj] * h
                  + datdi[2, jj] * p + datdi[3, jj] * zns
                  + datdi[4, jj] * ps) * deg2rad
        dr = datdi[5, jj] * (3.0 * sinphi ** 2 - 1.0) / 2.0 * np.cos(thetaf) \
            + datdi[7, jj] * (3.0 * sinphi ** 2 - 1.0) / 2.0 \
            * np.sin(thetaf)
        dn = datdi[6, jj] * (cosphi * sinphi * 2.0) * np.cos(thetaf) \
            + datdi[8, jj] * (cosphi * sinphi * 2.0) * np.sin(thetaf)
        de = 0.0
        dr_tot = dr_tot + dr
        dn_tot = dn_tot + dn
        xcorsta.x += dr * cosla * cosphi - de * sinla \
            - dn * sinphi * cosla
        xcorsta.y += dr * sinla * cosphi + de * cosla \
            - dn * sinphi * sinla
        xcorsta.z += dr * sinphi + dn * cosphi

    xcorsta.x /= 1000.
    xcorsta.y /= 1000.
    xcorsta.z /= 1000.
    return xcorsta


def step2diu(xsta: XYZ, fhr: float, t: float) -> XYZ:
    s = 218.31664563 + 481267.88194 * t - 0.0014663889 * t * t \
        + 0.00000185139 * t ** 3
    tau = fhr * 15.0 + 280.4606184 + 36000.7700536 * t \
        + 0.00038793 * t * t - 0.0000000258 * t ** 3 - s
    pr = 1.396971278 * t + 0.000308889 * t * t \
        + 0.000000021 * t ** 3 + 0.000000007 * t ** 4
    s = s + pr
    h = 280.46645 + 36000.7697489 * t + 0.00030322222 * t * t \
        + 0.000000020 * t ** 3 - 0.00000000654 * t ** 4
    p = 83.35324312 + 4069.01363525 * t - 0.01032172222 * t * t \
        - 0.0000124991 * t ** 3 + 0.00000005263 * t ** 4
    zns = 234.95544499 + 1934.13626197 * t - 0.00207561111 * t * t \
        - 0.00000213944 * t ** 3 + 0.00000001650 * t ** 4
    ps = 282.93734098 + 1.71945766667 * t + 0.00045688889 * t * t \
        - 0.00000001778 * t ** 3 - 0.00000000334 * t ** 4

    # reduce angles to between 0 and 360
    s = np.remainder(s, 360.0)
    tau = np.remainder(tau, 360.0)
    h = np.remainder(h, 360.0)
    p = np.remainder(p, 360.0)
    zns = np.remainder(zns, 360.0)
    ps = np.remainder(ps, 360.0)

    rsta = xsta.enorm8()
    sinphi = xsta.z / rsta
    cosphi = np.sqrt(xsta.x ** 2 + xsta.y ** 2) / rsta
    cos2phi = cosphi * cosphi - sinphi * sinphi

    cosla = xsta.x / cosphi / rsta
    sinla = xsta.y / cosphi / rsta
    zla = np.arctan2(xsta.y, xsta.x)
    xcorsta = XYZ()
    datdi = datdi_step2diu.T

    for jj in range(31):
        thetaf = (tau + datdi[0, jj] * s + datdi[1, jj] * h
                  + datdi[2, jj] * p + datdi[3, jj] * zns
                  + datdi[4, jj] * ps) * deg2rad
        dr = datdi[5, jj] * 2.0 * sinphi * cosphi * np.sin(thetaf + zla) \
            + datdi[6, jj] * 2.0 * sinphi * cosphi * np.cos(thetaf+zla)
        dn = datdi[7, jj] * cos2phi * np.sin(thetaf + zla) \
            + datdi[8, jj] * cos2phi * np.cos(thetaf + zla)
        de = datdi[7, jj] * sinphi * np.cos(thetaf + zla) \
            - datdi[8, jj] * sinphi * np.sin(thetaf + zla)
        xcorsta.x += dr * cosla * cosphi - de * sinla - dn * sinphi * cosla
        xcorsta.y += dr * sinla * cosphi + de * cosla - dn * sinphi * sinla
        xcorsta.z += dr * sinphi + dn * cosphi

    xcorsta.x /= 1000.
    xcorsta.y /= 1000.
    xcorsta.z /= 1000.
    return xcorsta


def st1l1(xsta: XYZ,
          xsun: XYZ,
          xmon: XYZ,
          fac2sun: float,
          fac2mon: float) -> XYZ:
    """
    corrections induced by the latitude dependence
    given by l^(1) in mahtews et al (1991)
    """
    l1d = 0.0012
    l1sd = 0.0024
    rsta = xsta.enorm8()
    sinphi = xsta.z / rsta
    cosphi = np.sqrt(xsta.x ** 2 + xsta.y ** 2) / rsta
    sinla = xsta.y / cosphi / rsta
    cosla = xsta.x / cosphi / rsta
    rmon = xmon.enorm8()
    rsun = xsun.enorm8()
    cos2phi = cosphi * cosphi - sinphi * sinphi

    # for the diurnal band
    l1 = l1d
    dnsun = -l1 * sinphi ** 2 * fac2sun * xsun.z \
        * (xsun.x * cosla + xsun.y * sinla) / rsun ** 2
    dnmon = -l1 * sinphi ** 2 * fac2mon * xmon.z \
        * (xmon.x * cosla + xmon.y * sinla) / rmon ** 2
    desun = l1 * sinphi * cos2phi * fac2sun * xsun.z * \
        (xsun.x * sinla - xsun.y * cosla) / rsun ** 2
    demon = l1 * sinphi * cos2phi * fac2mon * xmon.z * \
        (xmon.x * sinla - xmon.y * cosla) / rmon ** 2
    de = 3.0 * (desun + demon)
    dn = 3.0 * (dnsun + dnmon)
    xcorsta = XYZ(
        -de * sinla - dn * sinphi * cosla,
        de * cosla - dn * sinphi * sinla,
        dn * cosphi
    )

    # for the semi-diurnal band
    l1 = l1sd
    costwola = cosla ** 2 - sinla ** 2
    sintwola = 2.0 * cosla * sinla
    dnsun = -l1 / 2.0 * sinphi * cosphi * fac2sun * \
        ((xsun.x ** 2 - xsun.y ** 2) *
         costwola + 2.0 * xsun.x * xsun.y * sintwola) / rsun ** 2
    dnmon = -l1 / 2.0 * sinphi * cosphi * fac2mon * \
        ((xmon.x ** 2 - xmon.y ** 2) *
         costwola + 2.0 * xmon.x * xmon.y * sintwola) / rmon ** 2
    desun = -l1 / 2.0 * sinphi ** 2 * cosphi * fac2sun * \
        ((xsun.x ** 2 - xsun.y ** 2) *
         sintwola - 2.0 * xsun.x * xsun.y * costwola) / rsun ** 2
    demon = -l1 / 2.0 * sinphi ** 2 * cosphi * fac2mon * \
        ((xmon.x ** 2 - xmon.y ** 2) *
         sintwola - 2.0 * xmon.x * xmon.y * costwola) / rmon ** 2
    de = 3.0 * (desun + demon)
    dn = 3.0 * (dnsun + dnmon)
    xcorsta.x = xcorsta.x - de * sinla - dn * sinphi * cosla
    xcorsta.y = xcorsta.y + de * cosla - dn * sinphi * sinla
    xcorsta.z = xcorsta.z + dn * cosphi
    return xcorsta


def detide(xsta: XYZ,
           jul: ModJulDate,
           xsun: XYZ,
           xmon: XYZ) -> XYZ:
    """
    computation of tidal corrections of station displacements caused
    by lunar and solar gravitational attraction (UTC version)

    step 1 (here general degree 2 and 3 corrections +
            call st1idiu + call st1isem + call st1l1)
      + step 2 (call step2diu + call step2lon + call step2idiu)
    it has been decided that the step 3 un-correction for permanent tide
    would *not* be applied in order to avoid jump in the reference frame
    (this step 3 must added in order to get the mean tide station position
    and to be conformed with the iag resolution.)
    """
    h20 = 0.6078
    l20 = 0.0847
    h3 = 0.292
    l3 = 0.015

    # first, convert UTC time into TT time (and, bring leapflag into variable)
    tsecutc = jul.fmjd * 86400.0
    _, tsectt = utc2ttt(jul.mjd, tsecutc)
    fmjdtt = tsectt / 86400.0

    # float MJD in TT
    dmjdtt = jul.mjd + fmjdtt
    # days to centuries, TT
    t = (dmjdtt - 51544.0) / 36525.0
    # hours in the day, TT
    fhr = (dmjdtt - int(dmjdtt)) * 24.0

    # scalar product of station vector with sun/moon vector
    scs, rsta, rsun = sprod(xsta, xsun)
    scm, rsta, rmon = sprod(xsta, xmon)
    scsun = scs / rsta / rsun
    scmon = scm / rsta / rmon

    # computation of new h2 and l2
    cosphi = np.sqrt(xsta.x * xsta.x + xsta.y * xsta.y) / rsta
    h2 = h20 - 0.0006 * (1.0 - 3.0 / 2.0 * cosphi * cosphi)
    l2 = l20 + 0.0002 * (1.0 - 3.0 / 2.0 * cosphi * cosphi)

    # p2-term
    p2sun = 3.0 * (h2 / 2.0 - l2) * scsun * scsun - h2 / 2.0
    p2mon = 3.0 * (h2 / 2.0 - l2) * scmon * scmon - h2 / 2.0

    # p3-term
    p3sun = 5.0 / 2.0 * (h3 - 3.0 * l3) * scsun ** 3 + 3.0 / 2.0 \
        * (l3 - h3) * scsun
    p3mon = 5.0 / 2.0 * (h3 - 3.0 * l3) * scmon ** 3 + 3.0 / 2.0 \
        * (l3 - h3) * scmon

    # term in direction of sun/moon vector
    x2sun = 3.0 * l2 * scsun
    x2mon = 3.0 * l2 * scmon
    x3sun = 3.0 * l3 / 2.0 * (5.0 * scsun * scsun - 1.0)
    x3mon = 3.0 * l3 / 2.0 * (5.0 * scmon * scmon - 1.0)

    # factors for sun/moon
    mass_ratio_sun = 332945.943062
    mass_ratio_moon = 0.012300034
    re = 6378136.55
    fac2sun = mass_ratio_sun * re * (re / rsun) ** 3
    fac2mon = mass_ratio_moon * re * (re / rmon) ** 3
    fac3sun = fac2sun * (re / rsun)
    fac3mon = fac2mon * (re / rmon)

    # total displacement
    dxtide = XYZ()
    dxtide.x = fac2sun * (x2sun * xsun.x / rsun + p2sun * xsta.x / rsta) \
        + fac2mon * (x2mon * xmon.x / rmon + p2mon * xsta.x / rsta) \
        + fac3sun * (x3sun * xsun.x / rsun + p3sun * xsta.x / rsta) \
        + fac3mon * (x3mon * xmon.x / rmon + p3mon * xsta.x / rsta)

    dxtide.y = fac2sun * (x2sun * xsun.y / rsun + p2sun * xsta.y / rsta) \
        + fac2mon * (x2mon * xmon.y / rmon + p2mon * xsta.y / rsta) \
        + fac3sun * (x3sun * xsun.y / rsun + p3sun * xsta.y / rsta) \
        + fac3mon * (x3mon * xmon.y / rmon + p3mon * xsta.y / rsta)

    dxtide.z = fac2sun * (x2sun * xsun.z / rsun + p2sun * xsta.z / rsta) \
        + fac2mon * (x2mon * xmon.z / rmon + p2mon * xsta.z / rsta) \
        + fac3sun * (x3sun * xsun.z / rsun + p3sun * xsta.z / rsta) \
        + fac3mon * (x3mon * xmon.z / rmon + p3mon * xsta.z / rsta)

    # corrections for the out-of-phase part of love numbers
    # (part h_2^(0)i and l_2^(0)i )
    # first, for the diurnal band

    xcorsta = st1idiu(xsta, xsun, xmon, fac2sun, fac2mon)
    dxtide.x += xcorsta.x
    dxtide.y += xcorsta.y
    dxtide.z += xcorsta.z

    # second, for the semi-diurnal band
    xcorsta = st1isem(xsta, xsun, xmon, fac2sun, fac2mon)
    dxtide.x += xcorsta.x
    dxtide.y += xcorsta.y
    dxtide.z += xcorsta.z

    # corrections for the latitude dependence of love numbers (part l^(1) )
    xcorsta = st1l1(xsta, xsun, xmon, fac2sun, fac2mon)
    dxtide.x += xcorsta.x
    dxtide.y += xcorsta.y
    dxtide.z += xcorsta.z

    # second, the diurnal band corrections,
    # (in-phase and out-of-phase frequency dependence):
    xcorsta = step2diu(xsta, fhr, t)
    dxtide.x += xcorsta.x
    dxtide.y += xcorsta.y
    dxtide.z += xcorsta.z

    # corrections for the long-period band,
    # (in-phase and out-of-phase frequency dependence):
    xcorsta = step2lon(xsta, fhr, t)
    dxtide.x += xcorsta.x
    dxtide.y += xcorsta.y
    dxtide.z += xcorsta.z

    return dxtide


def solid_point(pt: LLH,
                date: datetime.date,
                step_sec: int) -> tuple[npt.ArrayLike, npt.ArrayLike]:
    """
    calculate SET at given location for one day with
    step_sec seconds resolution
    """
    glad = pt.lat
    glod = pt.lon
    iyr = int(date.year)
    imo = int(date.month)
    idy = int(date.day)

    nloop = 60 * 60 * 24 // step_sec
    secs = np.zeros(nloop)
    tide = np.zeros((nloop, 3))
    tide_e = tide[:, 0]
    tide_n = tide[:, 1]
    tide_u = tide[:, 2]

    # check inputs section
    if not (-90 < glad < 90):
        raise ValueError(f'ERROR: lat NOT in [-90,+90]: {glad}')

    if not (-360 < glod < 360):
        raise ValueError(f'ERROR: lon NOT in [-360,+360]: {glod}')

    if not (1901 < iyr < 2099):
        raise ValueError(f'ERROR: year NOT in [1901-2099]: {iyr}')

    # position of observing point (positive East)
    glod += (glod < 0) * 360.

    gla0 = glad / rad
    glo0 = glod / rad
    xsta = LLH(gla0, glo0, 0.).geoxyz()

    # here comes the sun  (and the moon)  (go, tide!)
    # UTC time system
    civ = CivDate(iyr, imo, idy, 0, 0, 0.0)
    jul = civ.civmjd()
    civ_norm = jul.mjdciv()
    jul = civ_norm.civmjd()

    # loop over time
    tdel2 = 1.0 / float(nloop)
    for iloop in range(nloop):
        # mjd/fmjd in UTC
        rsun = sunxyz(jul)
        rmoon = moonxyz(jul)
        etide = detide(xsta, jul, rsun, rmoon)

        # determine local geodetic horizon components (topocentric)

        # tide vector
        uvw = etide.rge(LLH(gla0, glo0, 0.))
        civ = jul.mjdciv()

        tsec = civ.secs_of_day

        secs[iloop] = tsec
        tide_e[iloop] = uvw.y
        tide_n[iloop] = uvw.x
        tide_u[iloop] = uvw.z

        # update fmjd for the next round
        jul.fmjd += tdel2

        # force 1 sec. granularity
        jul.fmjd = (round(jul.fmjd * 86400.0)) / 86400.0

    return secs, tide


def solid_grid(
    dtime: datetime.datetime,
    lats: npt.ArrayLike,
    lons: npt.ArrayLike
) -> npt.ArrayLike:
    """
    Computes tides on a grid defined by lats and lons
    """
    iyr = int(dtime.year)
    imo = int(dtime.month)
    idy = int(dtime.day)
    ihh = int(dtime.hour)
    imm = int(dtime.minute)
    iss = int(dtime.second)

    if not (1901 < iyr < 2099):
        raise ValueError(f'ERROR: year NOT in [1901-2099]: {iyr}')

    if np.any(np.logical_or(lats < -90.0, lats > 90.0)):
        raise ValueError("Latitudes outside range of (-90, 90)")

    if np.any(np.logical_or(lons < -360.0, lons > 360.0)):
        raise ValueError("Longitudes outside range of (-360, 360)")

    nlat = lats.size
    nlon = lons.size

    tides = np.zeros((3, nlat, nlon))
    tide_e = tides[0]
    tide_n = tides[1]
    tide_u = tides[2]

    # Normalize time here- epoch doesn't change
    # No need to do this in a loop
    civ = CivDate(iyr, imo, idy, ihh, imm, iss)
    jul = civ.civmjd()
    civ = jul.mjdciv()
    rsun = sunxyz(jul)
    rmoon = moonxyz(jul)

    for ilat, glad in enumerate(lats):
        for ilon, glod in enumerate(lons):

            # position of observing point (positive East)
            glod += (glod < 0) * 360.

            gla0 = glad / rad
            glo0 = glod / rad
            pt = LLH(gla0, glo0, 0.)
            xsta = pt.geoxyz()

            # here comes the sun  (and the moon)  (go, tide!)
            # mjd/fmjd in UTC
            etide = detide(xsta, jul, rsun, rmoon)

            # determine local geodetic horizon components (topocentric)
            # tide vector
            uvw = etide.rge(LLH(gla0, glo0, 0.))

            # Do not understand this line - why is this needed
            # call mjdciv(mjd,fmjd+0.001d0/86400.d0,
            # iyr,imo,idy,ihr,imn,sec-0.001d0)

            # write output respective arrays
            tide_e[ilat, ilon] = uvw.y
            tide_n[ilat, ilon] = uvw.x
            tide_u[ilat, ilon] = uvw.z

    return tides
