#!/usr/bin/env python3
#
# fp.py - flight planning main program 
#
import sys
import pickle
import Aircraft
import Geodesic
from Geodesic import DEG_TO_RAD, RAD_TO_DEG
import MagVar
import re
from math import sin,asin,cos,pow

def die( msg ):
    print( f'ERROR: {msg}' )
    sys.exit( 1 )

#--------------------------------------------------------------
# Read in rawdata which is indexed by airport/waypoint id
#--------------------------------------------------------------
f = open( 'rawdata/rawdata.dat', 'rb' )
rawdata = pickle.load( f )
f.close()

#--------------------------------------------------------------
# Parse Arguments
#--------------------------------------------------------------
type       = 'C172S'
tail       = ''
name       = '<lat,lon>'        # name of checkpoint for lat,lon only
ias        = 110
ia         = 0                  # indicated altitude (start on ground)
alt        = 29.92              # altimeter setting
flaps      = 0                  # flaps setting in degrees
wind_dir   = 0
wind_speed = 0
oat        = 15
fuel_gal   = 0                  # 0 = use fuel_gal_max for type
fuel_gal_taxi = 0               # 0 = use default fuel for startup+taxi
fuel_gph   = 0                  # 0 = use default GPH
runway     = 36                 # takeoff runway heading
route      = []

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if arg == '-p':
        id = sys.argv[i].upper()
        i += 1
        if id in rawdata:
            lat = rawdata[id]['lat']
            lon = rawdata[id]['lon']
            if ia == 0: ia = rawdata[id]['elevation']
            name = id
        else:
            # might be lat,lon 
            matches = re.match( r'^(-?\d+\.\d+),(-?\d+\.\d+)$', id );
            if not matches: die( f'unknown airport/waypoint and not a proper lat/lon: {id}' )
            lat = float(matches.group(1))
            lon = float(matches.group(2))
            id = ''
        route.append( { 'id': id, 'name': name, 'lat': lat, 'lon': lon, 'ias': ias, 'ia': ia, 'alt': alt, 'flaps': flaps,
                        'wind_dir': wind_dir, 'wind_speed': wind_speed, 'oat': oat,
                        'fuel_gph': fuel_gph } )
    elif arg == '-t':
        type = sys.argv[i].upper()
        i += 1
        if type not in Aircraft.types: die( f'unknown aircraft type: {type}' ) 
        if len(route) > 0: die( '-t <aircraft type> option must occur before first -p option' )
    elif arg == '-tail':
        tail = sys.argv[i].upper()
        i += 1
        if tail not in Aircraft.tails : die( f'unknown aircraft tail number: {tail}' ) 
        if len(route) > 0: die( '-tail <tail number> option must occur before first -p option' )
    elif arg == '-name':
        name = sys.argv[i]
        i += 1
    elif arg == '-ias':
        ias = float(sys.argv[i])
        i += 1
    elif arg == '-altitude' or arg == '-ia':
        ia = float(sys.argv[i])
        i += 1
    elif arg == '-altimeter' or arg == '-alt':
        alt = float(sys.argv[i])
        i += 1
    elif arg == '-flaps': 
        flaps = float(sys.argv[i])
        i += 1
    elif arg == '-wd': 
        wind_dir = float(sys.argv[i])
        i += 1
    elif arg == '-ws': 
        wind_speed = float(sys.argv[i])
        i += 1
    elif arg == '-oat':
        oat = float(sys.argv[i])
        i += 1
    elif arg == '-fuel_gal':
        fuel_gal = float(sys.argv[i])
        i += 1
    elif arg == '-fuel_gal_taxi':
        fuel_gal_taxi = float(sys.argv[i])
        i += 1
    elif arg == '-fuel_gph':
        fuel_gph = float(sys.argv[i])
        i += 1
    elif arg == '-runway':
        runway = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {sys.argv[i]}' )

#--------------------------------------------------------------
# Defaults Based on Aircraft Type
#--------------------------------------------------------------
if type not in Aircraft.types: die( f'unknown aircraft type: {type}' )
type_info = Aircraft.types[type]
if tail != "":
    if tail not in Aircraft.tails: die( f'unknown tail number: {tail}' )
    tail_info = Aircraft.tails[tail]
else:
    tail_info = None
if fuel_gal <= 0: fuel_gal = type_info['fuel_gal_max']
if fuel_gal_taxi <= 0: fuel_gal_taxi = type_info['fuel_gal_taxi']
if fuel_gph <= 0: fuel_gph = type_info['fuel_gph']         # TODO: need to look at tables for this

#--------------------------------------------------------------
# Analyze Route
#--------------------------------------------------------------
lapserate = 0.0019812		        # degrees / foot std. lapse rate C° in to K° result
tempcorr = 273.15			# Kelvin
stdtemp0 = 288.15			# Kelvin

# next 3 functions transcribed from http://indoavis.co.id/main/tas.html Javascript code:
#
def calc_PA( IA, ALT ):
    #std_ALT = 29.92
    #xx = std_ALT / 29.92126
    #PA = IA + 145442.2*(1 - pow(xx, 0.190261))
    PA = IA + 1000*(29.92 - ALT)
    return PA

def calc_DA( PA, OAT ):
    stdtemp = stdtemp0 - PA*lapserate
    Tratio = stdtemp / lapserate
    xx = stdtemp / (OAT + tempcorr)	
    DA = PA + Tratio*(1 - pow(xx, 0.234969))
    return DA

def calc_TAS( CAS, DA ):
    aa = DA * lapserate                 # Calculate DA temperature
    bb = stdtemp0 - aa			# Correct DA temp to Kelvin
    cc = bb / stdtemp0			# Temperature ratio
    cc1 = 1 / 0.234969			# Used to find .235 root next
    dd = pow(cc, cc1)			# Establishes Density Ratio
    dd = pow(dd, .5)			# For TAS, square root of DR
    ee = 1 / dd				# For TAS; 1 divided by above
    TAS = ee * CAS
    return TAS

def lerp( f, v0, v1 ):
    return (1-f)*v0 + f*v1

def find_closest_row( a, table, except_row=-1, a_col=0, a_modulo=0 ):
    if a_modulo != 0:
        a = a % a_modulo
    r = -1
    rd = 1e20
    for i in range(len(table)):
        if i == except_row: continue
        ai = table[i][a_col]
        if a_modulo != 0:
            ai = ai % a_modulo
        d = abs(ai - a)
        if r < 0 or d < rd:
            rd = d
            r = i
    return r

def interpolate( a, a0, a1, b0, b1, a_modulo=0, ab_modulo=0 ):
    if a_modulo != 0:
        a  = a  % a_modulo
        if a0 >= a_modulo:
            a0 -= a_modulo    
            b0 -= ab_modulo 
        if a1 >= a_modulo:
            a1 -= a_modulo    
            b1 -= ab_modulo 
    if a0 == a1: return b0
    if a0 < a1:
        if a < a0: die( f'interpolate() a={a} < a0={a0}' )
        f = (a - a0) / (a1 - a0)
        return lerp( f, b0, b1 )
    else:
        if a < a1: die( f'interpolate() a={a} < a0={a0}' )
        f = (a - a1) / (a0 - a1)
        return lerp( f, b1, b0 )

def interpolate_closest_rows( a, table, b_col=1, a_col=0, a_modulo=0, ab_modulo=0 ):
    r0 = find_closest_row( a, table, -1, a_col, a_modulo )
    r1 = find_closest_row( a, table, r0, a_col, a_modulo )
    a0 = table[r0][a_col] 
    a1 = table[r1][a_col]
    b0 = table[r0][b_col]
    b1 = table[r1][b_col]
    return interpolate( a, a0, a1, b0, b1, a_modulo, ab_modulo )

def calc_CAS( IAS, FLAPS, table ):
    for i in range(len(table)>>1):
        if table[i*2+0] >= FLAPS:
            return interpolate_closest_rows( IAS, table[i*2+1] )
    die( f'flaps={FLAPS} has no relevant entry in the CAS table' )

def calc_DEV( MH, table ):
    return interpolate_closest_rows( MH, table, 1, 0, 360, 360 ) - MH

MagVar.reinit()
if len( route ) < 2: die( 'route must contain at least two points' )
print( f'CHECKPOINT         LAT    LON  TC   IA   ALT  WD WS OAT   IAS CAS TAS   WCA  TH MV  MH DEV  CH       D  DTOT    GS   ETE   ETA   GPH  GAL  REM' )
print( f'----------------------------------------------------------------------------------------------------------------------------------------------' )
DTOT = 0
ETA = 0
for i in range( 0, len(route) ):
    fm = route[0] if i == 0 else route[i-1]
    to = route[i]
    TO_NAME = to['name']

    FM_LAT = fm['lat']
    FM_LON = fm['lon']
    TO_LAT = to['lat']
    TO_LON = to['lon']
    FM_IAS = fm['ias']
    TO_IAS = to['ias']
    FM_WS  = fm['wind_speed']
    TO_WS  = to['wind_speed']
    FM_WD  = fm['wind_dir']
    TO_WD  = to['wind_dir']
    FM_IA  = fm['ia']
    TO_IA  = to['ia']
    FM_ALT = fm['alt']
    TO_ALT = to['alt']
    FM_FLAPS = fm['flaps']
    TO_FLAPS = to['flaps']
    FM_OAT = fm['oat']
    TO_OAT = to['oat']
    FM_GPH = fm['fuel_gph'] if fm['fuel_gph'] > 0 else fuel_gph
    TO_GPH = to['fuel_gph'] if to['fuel_gph'] > 0 else fuel_gph

    D    = Geodesic.distance( FM_LAT, FM_LON, TO_LAT, TO_LON )
    DTOT+= D
    TC   = (runway * 10) if i == 0 else Geodesic.initial_bearing( FM_LAT, FM_LON, TO_LAT, TO_LON )
    IAS  = TO_IAS 
    FLAPS= TO_FLAPS
    CAS  = calc_CAS( IAS, FLAPS, type_info['airspeed_calibration'] )
    WS   = TO_WS
    WD   = TO_WD
    WA   = WD + 180
    while WA > 360: WA -= 360
    WTA  = TC - WA
    DIA  = TO_IA
    IA   = TO_IA
    ALT  = TO_ALT
    OAT  = TO_OAT
    PA   = calc_PA( IA, ALT )
    DA   = calc_DA( PA, OAT )
    TAS  = calc_TAS( CAS, DA )
    WCA  = RAD_TO_DEG*asin( WS * sin( DEG_TO_RAD*WTA ) / TAS )
    TH   = TC + WCA
    MV   = (-MagVar.today_magvar( FM_LAT, FM_LON ) + -MagVar.today_magvar( TO_LAT, TO_LON )) / 2.0
    MH   = TH + MV
    DEV  = calc_DEV( MH, tail_info['magnetic_deviation'] ) if tail_info else 0
    CH   = MH + DEV
    GS   = TAS*cos( DEG_TO_RAD*WCA ) + WS*cos( DEG_TO_RAD*WTA )
    ETE  = D/GS * 60.0
    ETA += ETE
    GPH  = TO_GPH
    GAL  = (ETE / 60.0 * GPH) if i != 0 else fuel_gal_taxi
    fuel_gal -= GAL

    print( f'{TO_NAME:15s} {TO_LAT:6.2f} {TO_LON:6.2f} {TC:3.0f} {IA:4.0f} {ALT:5.2f} {WD:3.0f} {WS:2.0f} {OAT:3.0f}   {IAS:3.0f} {CAS:3.0f} {TAS:3.0f}   {WCA:3.0f} {TH:3.0f} {MV:2.0f} {MH:3.0f} {DEV:3.0f} {CH:3.0f}   {D:5.1f} {DTOT:5.1f} {GS:5.1f} {ETE:5.1f} {ETA:5.1f}  {GPH:4.1f} {GAL:4.1f} {fuel_gal:4.1f}' )

print()
print( 'Airport Elevations' )
print( '------------------' )
for i in range( 0, len(route) ):
    id = route[i]['id']
    if id != '':
        elevation = rawdata[id]['elevation']
        print( f'{id:5s} {elevation:4.0f}' )
