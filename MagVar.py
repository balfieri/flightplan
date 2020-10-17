# MagVar.py - computes magnetic variation for a given lat/lon and date
# 
# This is a Python port of JS code from https://github.com/dpyeates/magvar
#
from datetime import date
from math import pi,sqrt,sin,cos,tan,asin,acos,atan2
from Geodesic import DEG_TO_RAD, RAD_TO_DEG

def yymmdd_to_julian_days( yy, mm, dd ):
    secs = 0
    return secs / 86400000 - getTimezoneOffset() / 1440 + 2440587.5

def createArray(len0, len1=0, len2=0):
    a = []
    for i in range(len0):
        if len1 == 0:
            a[i] = 0.0
        else:
            a[i] = []
            for j in range(len1):
                a[i][j] = []
                if len2 == 0:
                    a[i][j] = 0.0
                else:
                    for k in range(len2):
                        a[i][j][k] = 0.0
    return a

def reinit():
    global julian_days_now, julian_days_2020
    global nmax, a, f, b, r_0
    global gnm_wmm2020, hnm_wmm2020, gtnm_wmm2020, htnm_wm2020
    global P, DP, gnm, hnm, sm, cm, root, roots

    d = datetime.date.today()
    julian_days_now = yymmdd_to_julian_days( d.year, d.month, d.day )
    nmax = 12
    a = 6378.137                        # semi-major axis [equatorial radius] of WGS84 ellipsoid 
    f = 1.0 / 298.257223563             # inverse flattening IAU66 ellipsoid
    b = 6356.7523142                    # semi-minor axis referenced to the WGS84 ellipsoid
    r_0 = 6371.2                        # "mean radius" for spherical harmonic expansion 
    julian_days_2020 = 2458850
    gnm_wmm2020 = [
        [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 0
        ],
        [
            -29404.5, -1450.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 1
        ],
        [
            -2500.0, 2982.0, 1676.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 2
        ],
        [
            1363.9, -2381.0, 1236.2, 525.7, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 3
        ],
        [
            903.1, 809.4, 86.2, -309.4, 47.9, 0, 0, 0, 0, 0, 0, 0, 0 # 4
        ],
        [
            -234.4, 363.1, 187.8, -140.7, -151.2, 13.7, 0, 0, 0, 0, 0, 0, 0 # 5
        ],
        [
            65.9, 65.6, 73.0, -121.5, -36.2, 13.5, -64.7, 0, 0, 0, 0, 0, 0 # 6
        ],
        [
            80.6, -76.8, -8.3, 56.5, 15.8, 6.4, -7.2, 9.8, 0, 0, 0, 0, 0 # 7
        ],
        [
            23.6, 9.8, -17.5, -0.4, -21.1, 15.3, 13.7, -16.5, -0.3, 0, 0, 0, 0 # 8
        ],
        [
            5.0, 8.2, 2.9, -1.4, -1.1, -13.3, 1.1, 8.9, -9.3, -11.9, 0, 0, 0 # 9
        ],
        [
            -1.9, -6.2, -0.1, 1.7, -0.9, 0.6, -0.9, 1.9, 1.4, -2.4, -3.9, 0, 0 # 10
        ],
        [
            3.0, -1.4, -2.5, 2.4, -0.9, 0.3, -0.7, -0.1, 1.4, -0.6, 0.2, 3.1, 0 # 11
        ],
        [
            -2.0, -0.1, 0.5, 1.3, -1.2, 0.7, 0.3, 0.5, -0.2, -0.5, 0.1, -1.1, -0.3 # 12
        ]
    ]
    hnm_wmm2020 = [
        [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 // 0
        ], 
        [
            0, 4652.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 // 1
        ], 
        [
            0, -2991.6, -734.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 // 2
        ], 
        [
            0, -82.2, 241.8, -542.9, 0, 0, 0, 0, 0, 0, 0, 0, 0 // 3
        ], 
        [
            0, 282.0, -158.4, 199.8, -350.1, 0, 0, 0, 0, 0, 0, 0, 0 // 4
        ], 
        [
            0, 47.7, 208.4, -121.3, 32.2, 99.1, 0, 0, 0, 0, 0, 0, 0 // 5
        ], 
        [
            0, -19.1, 25.0, 52.7, -64.4, 9.0, 68.1, 0, 0, 0, 0, 0, 0 // 6
        ], 
        [
            0, -51.4, -16.8, 2.3, 23.5, -2.2, -27.2, -1.9, 0, 0, 0, 0, 0 // 7
        ], 
        [
            0, 8.4, -15.3, 12.8, -11.8, 14.9, 3.6, -6.9, 2.8, 0, 0, 0, 0 // 8
        ], 
        [
            0, -23.3, 11.1, 9.8, -5.1, -6.2, 7.8, 0.4, -1.5, 9.7, 0, 0, 0 // 9
        ], 
        [
            0, 3.4, -0.2, 3.5, 4.8, -8.6, -0.1, -4.2, -3.4, -0.1, -8.8, 0, 0 // 10
        ], 
        [
            0, -0, 2.6, -0.5, -0.4, 0.6, -0.2, -1.7, -1.6, -3.0, -2.0, -2.6, 0 // 11
        ], 
        [
            0, -1.2, 0.5, 1.3, -1.8, 0.1, 0.7, -0.1, 0.6, 0.2, -0.9, -0.0, 0.5 // 12
        ]
    ]
    gtnm_wmm2020 = [
        [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 0
        ], 
        [
            6.7, 7.7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 1
        ], 
        [
            -11.5, -7.1, -2.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 2
        ], 
        [
            2.8, -6.2, 3.4, -12.2, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 3
        ], 
        [
            -1.1, -1.6, -6.0, 5.4, -5.5, 0, 0, 0, 0, 0, 0, 0, 0 # 4
        ], 
        [
            -0.3, 0.6, -0.7, 0.1, 1.2, 1.0, 0, 0, 0, 0, 0, 0, 0 # 5
        ], 
        [
            -0.6, -0.4, 0.5, 1.4, -1.4, 0, 0.8, 0, 0, 0, 0, 0, 0 # 6
        ], 
        [
            -0.1, -0.3, -0.1, 0.7, 0.2, -0.5, -0.8, 1, 0, 0, 0, 0, 0 # 7
        ], 
        [
            -0.1, 0.1, -0.1, 0.5, -0.1, 0.4, 0.5, 0, 0.4, 0, 0, 0, 0 # 8
        ], 
        [
            -0.1, -0.2, -0, 0.4, -0.3, 0, 0.3, -0, 0, -0.4, 0, 0, 0 # 9
        ], 
        [
            0, -0, -0, 0.2, -0.1, -0.2, -0, -0.1, -0.2, -0.1, -0, 0, 0 # 10
        ], 
        [
            0, -0.1, 0, 0, 0, -0.1, 0, 0, -0.1, -0.1, -0.1, -0.1, 0 # 11
        ], 
        [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.1 # 12
        ]
    ]
    htnm_wmm2020 = [
      [
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 0
      ], 
      [
          0, -25.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 1
      ], 
      [
          0, -30.2, -23.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 2
      ], 
      [
          0, 5.7, -1.0, 1.1, 0, 0, 0, 0, 0, 0, 0, 0, 0 # 3
      ], 
      [
          0, 0.2, 6.9, 3.7, -5.6, 0, 0, 0, 0, 0, 0, 0, 0 # 4
      ], 
      [
          0, 0.1, 2.5, -0.9, 3.0, 0.5, 0, 0, 0, 0, 0, 0, 0 # 5
      ], 
      [
          0, 0.1, -1.8, -1.4, 0.9, 0.1, 1.0, 0, 0, 0, 0, 0, 0 # 6
      ], 
      [
          0, 0.5, 0.6, -0.7, -0.2, -1.2, 0.2, 0.3, 0, 0, 0, 0, 0 # 7
      ], 
      [
          0, -0.3, 0.7, -0.2, 0.5, -0.3, -0.5, 0.4, 0.1, 0, 0, 0, 0 # 8
      ], 
      [
          0, -0.3, 0.2, -0.4, 0.4, 0.1, -0, -0.2, 0.5, 0.2, 0, 0, 0 # 9
      ], 
      [
          0, -0, 0.1, -0.3, 0.1, -0.2, 0.1, -0, -0.1, 0.2, -0, 0, 0 # 10
      ], 
      [
          0, -0, 0.1, 0, 0.2, -0, 0, 0.1, -0, -0.1, 0, -0, 0 # 11
      ], 
      [
          0, -0, 0, -0.1, 0.1, -0, 0, -0, 0.1, -0, -0, 0, -0.1 # 12
      ]
    ]
    P = createArray(13, 13)
    DP = createArray(13, 13)
    gnm = createArray(13, 13)
    hnm = createArray(13, 13)
    sm = createArray(13)
    cm = createArray(13)
    root = createArray(13)
    roots = createArray(13, 13, 2)
    for n in range(2, nmax+1):
        root[n] = sqrt((2.0 * n - 1.0) / (2.0 * n))
    for m in range(nmax+1):
        mm = m * m
        for n in range(max(m + 1, 2), nmax+1):
            roots[m][n][0] = sqrt((n - 1.0) * (n - 1.0) - mm)
            roots[m][n][1] = 1.0 / sqrt(n * n - mm)

# calculateMagVar
# Given a date in julian days, latitude, longitude and height, return variation (in degrees)
# N and E latitude and longitude are positive values, South and West negative.
# @param {number} julian_days: the current number of days since epoch 0h Jan 1, 1950.
# @param {number} latIn: the latitude in degrees of the point we want to obtain the magnetic variation.
# @param {number} lonIn: the longitude in degrees of the point we want to obtain the magnetic variation.
# @param {number} h: the height in km above mean sea level of the point we want to obtain the magnetic variation.
# @returns {number} magnetic variation at the given coordinates and height.
#
def calculateMagVar( julian_days, latIn, lonIn, h ):
    lat = DEG_TO_RAD*latIn
    lon = DEG_TO_RAD*lonIn
    sinlat = sin( lat )
    coslat = cos( lat )
    mm = 0.0

    # convert to geocentric
    # is effective radius 
    sr = sqrt(a * a * coslat * coslat + b * b * sinlat * sinlat)

    # theta is geocentric co-latitude 
    theta = atan2(
        coslat * (h * sr + a * a),
        sinlat * (h * sr + b * b)
    )

    # r is geocentric radial distance 
    r = h * h + \
        2.0 * h * sr + \
        (a * a * a * a - \
            (a * a * a * a - b * b * b * b) * \
            sinlat * \
            sinlat) / \
        (a * a - (a * a - b * b) * sinlat * sinlat) 
    r = sqrt(r)
    c = cos(theta)
    s = sin(theta)

    # protect against zero divide at geographic poles 
    inv_s = 1.0e8 if s == 0 else 1.0 / s

    # zero out arrays 
    for n in range(nmax+1):
        for m in range(nmax+1):
            P[n][m] = 0.0
            DP[n][m] = 0.0

    # diagonal elements 
    P[0][0] = 1.0
    P[1][1] = s
    DP[0][0] = 0.0
    DP[1][1] = c
    P[1][0] = c
    DP[1][0] = -s

    for n in range(2, nmax+1):
        P[n][n] = P[n - 1][n - 1] * s * root[n]
        DP[n][n] = (DP[n - 1][n - 1] * s + P[n - 1][n - 1] * c) * root[n]

    # lower triangle 
    for m in range(nmax+1):
        for n in range(max(m+1,2), nmax+1):
            P[n][m] = \
                (P[n - 1][m] * c * (2.0 * n - 1) - P[n - 2][m] * roots[m][n][0]) * \
                roots[m][n][1]
            DP[n][m] = \
                ((DP[n - 1][m] * c - P[n - 1][m] * s) * (2.0 * n - 1) - \
                    DP[n - 2][m] * roots[m][n][0]) * \
                roots[m][n][1]

    yearfrac = (julian_days - julian_days_2020) / 365.25
    for n in range(1, nmax+1):
        for m in range(nmax+1):
            gnm[n][m] = gnm_wmm2020[n][m] + yearfrac * gtnm_wmm2020[n][m]
            hnm[n][m] = hnm_wmm2020[n][m] + yearfrac * htnm_wmm2020[n][m]

    # compute sm (sin(m lon) and cm (cos(m lon)) 
    for m in range(nmax+1):
        sm[m] = sin( m * lon )
        cm[m] = cos( m * lon )

    # compute B fields 
    B_r = 0.0
    B_theta = 0.0
    B_phi = 0.0
    fn_0 = r_0 / r
    fn = fn_0 * fn_0

    c1_n = 0.0
    c2_n = 0.0
    c3_n = 0.0
    tmp = 0.0
    for n in range(1, nmax+1):
        c1_n = 0
        c2_n = 0
        c3_n = 0
        for m in range(n+1):
            tmp = gnm[n][m] * cm[m] + hnm[n][m] * sm[m]
            c1_n += tmp * P[n][m]
            c2_n += tmp * DP[n][m]
            c3_n += m * (gnm[n][m] * sm[m] - hnm[n][m] * cm[m]) * P[n][m]
        fn *= fn_0
        B_r += (n + 1) * c1_n * fn
        B_theta -= c2_n * fn
        B_phi += c3_n * fn * inv_s

    # Find geodetic field components: 
    psi = theta - (pi / 2.0 - lat)
    sinpsi = sin( psi )
    cospsi = cos( psi )
    X = -B_theta * cospsi - B_r * sinpsi
    Y = B_phi
    Z = B_theta * sinpsi - B_r * cospsi

    # find variation in radians 
    # return zero variation at magnetic pole X=Y=0.
    # E is positive 
    return RAD_TO_DEG*atan2(Y, X) if X != 0.0 or Y != 0.0 else 0.0

# get
# Given a latitude and longitude position and optional height in metres above mean sea level,
# return magnetic variation in degrees for the current date.
# N and E latitude and longitude are positive values, S and W negative.
# @param {number} lat: the latitude in degrees of the point we want to obtain the magnetic variation.
# @param {number} lon: the longitude in degrees of the point we want to obtain the magnetic variation.
# @param {number} h: the height in km above mean sea level of the point we want to obtain the magnetic variation.
# @returns {number} magnetic variation at the given coordinates and height for the current date.
#
def get( lat, lon, h=0 ):
    return calculateMagVar( julian_days_now, lat, lon, h / 100 )
