#!/usr/local/bin/python3 
#
# fp.py - flight planning main program 
#
import sys
import pickle
import Geodesic

def die( msg ):
    print( f'ERROR: {msg}' )
    sys.exit( 1 )

#--------------------------------------------------------------
# Known Aircraft Types and Their Characteristics
#--------------------------------------------------------------
types = { 'C172S': {} }

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
altitude   = 3000
wind_dir   = 0
wind_speed = 0
route      = []

i = 1
while i < len( sys.argv ):
    arg = sys.argv[i]
    i += 1
    if arg == '-p':
        id = sys.argv[i].upper()
        i += 1
        if id in rawdata:
            route.append( { 'id': id, 'lat': rawdata[id]['lat'], 'lon': rawdata[id]['lon'], 'altitude': altitude, 'wind_dir': wind_dir, 'wind_speed': wind_speed } )
        else:
            die( f'unknown airport/waypoint: {id}' )
    elif arg == '-t':
        type = sys.argv[i].upper()
        i += 1
        if type not in types: die( f'unknown aircraft type: {type}' ) 
        if len(route) > 0: die( '-t <aircraft type> option must occur before first -p option' )
    elif arg == '-a':
        altitude = float(sys.argv[i])
        i += 1
    elif arg == '-wd': 
        wind_dir = float(sys.argv[i])
        i += 1
    elif arg == '-ws': 
        wind_speed = float(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {sys.argv[i]}' )

#--------------------------------------------------------------
# Analyze Route
#--------------------------------------------------------------
if len( route ) < 2: die( 'route must contain at least two points' )
for i in range( 1, len(route) ):
    fm = route[i-1]
    to = route[i]
    fm_id = fm['id']
    to_id = to['id']
    nm = Geodesic.distance( fm['lat'], fm['lon'], to['lat'], to['lon'] )
    course = Geodesic.initial_bearing( fm['lat'], fm['lon'], to['lat'], to['lon'] )
    print( f'{fm_id} to {to_id}: {nm} nm course={course}' )
