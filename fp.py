#!/usr/bin/env python3
#
# fp.py - flight planning main program 
#
import sys
import pickle
import Aircraft
import Geodesic
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
        else:
            # might be lat,lon 
            matches = re.match( r'^(-?\d+\.\d+),(-?\d+\.\d+)$', id );
            if not matches: die( f'unknown airport/waypoint and not a proper lat/lon: {id}' )
            lat = float(matches.group(1))
            lon = float(matches.group(2))
        route.append( { 'id': id, 'lat': lat, 'lon': lon, 'ias': ias, 'ia': ia, 'alt': alt, 'flaps': flaps,
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

def calc_CAS( IAS, FLAPS, table ):
    return IAS  # TODO

def calc_DEV( MH, table ):
    return MH   # TODO

MagVar.reinit()
if len( route ) < 2: die( 'route must contain at least two points' )
print( f'CHECKPOINT       TC   IA   ALT  WD  WS  OAT    PA    DA  IAS CAS TAS   WCA  TH MV  MH DEV  CH       D  DTOT  GS ETE ETA   GAL   REM' )
print( f'-----------------------------------------------------------------------------------------------------------------------------------' )
DTOT = 0
ETA = 0
for i in range( 0, len(route) ):
    fm = route[0] if i == 0 else route[i-1]
    to = route[i]
    fm_id = fm['id']
    to_id = to['id']

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
    TC   = Geodesic.initial_bearing( FM_LAT, FM_LON, TO_LAT, TO_LON )
    IAS  = (FM_IAS + TO_IAS) / 2.0
    FLAPS= (FM_FLAPS + TO_FLAPS) / 2.0
    CAS  = calc_CAS( IAS, FLAPS, type_info['airspeed_calibration'] )
    WS   = (FM_WS + TO_WS) / 2.0
    WD   = (FM_WD + TO_WD)/2.0
    WA   = WD + 180
    while WA > 360: WA -= 360
    WTA  = TC - WA
    IA   = (FM_IA + TO_IA) / 2.0
    ALT  = (FM_ALT + TO_ALT) / 2.0
    OAT  = (FM_OAT + TO_OAT) / 2.0
    PA   = calc_PA( IA, ALT )
    DA   = calc_DA( PA, OAT )
    TAS  = calc_TAS( CAS, DA )
    WCA  = asin( WS * sin( WTA ) / TAS )
    TH   = TC + WCA
    MV   = (-MagVar.today_magvar( FM_LAT, FM_LON ) + -MagVar.today_magvar( TO_LAT, TO_LON )) / 2.0 
    MH   = TH + MV
    DEV  = calc_DEV( MH, tail_info['magnetic_deviation'] ) if tail_info else 0
    CH   = MH + DEV
    GS   = TAS*cos( WCA ) + WS*cos( WTA )
    ETE  = D/GS * 60.0
    ETA += ETE
    GPH  = (FM_GPH + TO_GPH) / 2.0
    GAL  = (ETE / 60.0 * GPH) if i != 0 else fuel_gal_taxi
    fuel_gal -= GAL

    print( f'{to_id:15s} {TC:3.0f} {IA:4.0f} {ALT:5.2f} {WD:3.0f} {WS:3.0f} {OAT:4.1f} {PA:5.0f} {DA:5.0f}  {IAS:3.0f} {CAS:3.0f} {TAS:3.0f}   {WCA:3.0f} {TH:3.0f} {MV:2.0f} {MH:3.0f} {DEV:3.0f} {CH:3.0f}   {D:5.0f} {DTOT:5.0f} {GS:3.0f} {ETE:3.0f} {ETA:3.0f} {GAL:5.1f} {fuel_gal:5.1f}' )

