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
kias       = 110
altitude   = 3000
altimeter  = 29.92
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
            matches = re.match( r'^(-?\d+\.\d+),(-?\d+\.\d+)$', id );
            if not matches: die( f'unknown airport/waypoint and not a proper lat/lon: {id}' )
            lat = float(matches.group(1))
            lon = float(matches.group(2))
        route.append( { 'id': id, 'lat': lat, 'lon': lon, 'kias': kias, 'altitude': altitude, 'altimeter': altimeter, 
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
    elif arg == '-kias':
        kias = float(sys.argv[i])
        i += 1
    elif arg == '-altitude':
        altitude = float(sys.argv[i])
        i += 1
    elif arg == '-altimeter':
        altimeter = float(sys.argv[i])
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
aircraft = Aircraft.types[type]
if fuel_gal <= 0: fuel_gal = aircraft['fuel_gal_max']
if fuel_gal_taxi <= 0: fuel_gal_taxi = aircraft['fuel_gal_taxi']
if fuel_gph <= 0: fuel_gph = aircraft['fuel_gph']         # TODO: need to look at tables for this

#--------------------------------------------------------------
# Analyze Route
#--------------------------------------------------------------
print( f'Fuel gal before starting engine: {fuel_gal:.1f}' )
print( f'Fuel gal for startup and taxi:   {fuel_gal_taxi:.1f}' )
fuel_gal -= fuel_gal_taxi
print( f'Fuel gal after taxi:             {fuel_gal:.1f}' )

MagVar.reinit()
if len( route ) < 2: die( 'route must contain at least two points' )
for i in range( 1, len(route) ):
    fm = route[i-1]
    to = route[i]
    fm_id = fm['id']
    to_id = to['id']

    D    = Geodesic.distance( fm['lat'], fm['lon'], to['lat'], to['lon'] )
    TC   = Geodesic.initial_bearing( fm['lat'], fm['lon'], to['lat'], to['lon'] )
    KIAS = to['kias']
    KCAS = KIAS  # TODO
    WCA  = 0     # TODO
    KTAS = KCAS  # TODO
    TH   = TC + WCA
    MV   = -MagVar.today_magvar( to['lat'], to['lon'] )
    MH   = TH + MV
    DEV  = 0     # TODO
    CH   = MH + DEV
    GS   = KTAS  # TODO
    MIN  = D/GS * 60.0
    GPH  = to['fuel_gph'] if to['fuel_gph'] > 0 else fuel_gph
    GAL  = MIN / 60.0 * GPH
    fuel_gal -= GAL

    print( f'{fm_id} to {to_id}: D={D:.0f} TC={TC:.0f} KIAS={KIAS:.0f} KCAS={KCAS:.0f} WCA={WCA:.0f} KTAS={KTAS:.0f} TH={TH:.0f} MV={MV:.0f} MH={MH:.0f} DEV={DEV:.0f} CH={CH:.0f} GS={GS:.0f} MIN={MIN:.0f} GAL={GAL:.1f} GAL_REM={fuel_gal:.1f}' )

