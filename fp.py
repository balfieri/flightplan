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
        route.append( { 'id': id, 'lat': lat, 'lon': lon, 'kias': kias, 'altitude': altitude, 'altimeter': altimeter, 'wind_dir': wind_dir, 'wind_speed': wind_speed, 'oat': oat } )
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
    else:
        die( f'unknown option: {sys.argv[i]}' )

#--------------------------------------------------------------
# Analyze Route
#--------------------------------------------------------------
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

    # round them to nearest ints
    D    = int(round(D))
    TC   = int(round(TC))
    KIAS = int(round(KIAS))
    KCAS = int(round(KCAS))
    WCA  = int(round(WCA))
    KTAS = int(round(KTAS))
    TH   = int(round(TH))
    MV   = int(round(MV))
    MH   = int(round(MH))
    DEV  = int(round(DEV))
    CH   = int(round(CH))
    GS   = int(round(GS))
    MIN  = int(round(MIN))
    print( f'{fm_id} to {to_id}: D={D} TC={TC} KIAS={KIAS} KCAS={KCAS} WCA={WCA} KTAS={KTAS} TH={TH} MV={MV} MH={MH} DEV={DEV} CH={CH}, GS={GS} MIN={MIN}' )

