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
fuel_refill = False             # whether to refill before return flight
fuel_time_left_min = 60         # minimum fuel time left after landing (one hour)
runway     = 36                 # takeoff runway heading
row1_weight= 190                # assume 190lb pilot only
row2_weight= 0                  # assume no passengers
baggage1_weight = 0             # assume nothing in baggage area 1
baggage2_weight = 0             # assume nothing in baggage area 2
route      = []
runway_length_min = 2000        # minimum runway length for diversions
show_return= True               # show return route
alternate_airports = []
show_diversion_detail = False   # whether to include diversion airports in the airport information section

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
            matches = re.match( r'^(-?\d+\.\d+)[,\/](-?\d+\.\d+)$', id );
            if matches: 
                lat = float(matches.group(1))
                lon = float(matches.group(2))
            else:
                matches = re.match( r'^(\d\d)(\d\d)(N|S)(\d\d\d)(\d\d)(E|W)$', id );
                if not matches: die( f'unknown airport/waypoint and not a proper lat/lon: {id}' )
                lat = float(matches.group(1)) + float(matches.group(2))/60.0
                NS  = matches.group(3)
                if NS == 'S': lat = -lat
                lon = float(matches.group(4)) + float(matches.group(5))/60.0
                EW = matches.group(6)
                if EW == 'W': lon = -lon
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
    elif arg == '-fuel_refill':
        fuel_refill = int(sys.argv[i])
        i += 1
    elif arg == '-fuel_time_left_min':
        fuel_time_left_min = int(sys.argv[i])
        i += 1
    elif arg == '-runway':
        runway = int(sys.argv[i])
        i += 1
    elif arg == '-row1_weight':
        row1_weight = int(sys.argv[i])
        i += 1
    elif arg == '-row2_weight':
        row2_weight = int(sys.argv[i])
        i += 1
    elif arg == '-baggage1_weight':
        baggage1_weight = int(sys.argv[i])
        i += 1
    elif arg == '-baggage2_weight':
        baggage2_weight = int(sys.argv[i])
        i += 1
    elif arg == '-runway_length_min':
        runway_length_min = int(sys.argv[i])
        i += 1
    elif arg == '-show_return':
        show_return = int(sys.argv[i])
        i += 1
    elif arg == '-alternate':
        id = sys.argv[i].upper()
        if id not in rawdata: die( f'unknown alternate airport: {id}' )
        alternate_airports.append( id )
        i += 1
    elif arg == '-show_diversion_detail':
        show_diversion_detail = int(sys.argv[i])
        i += 1
    else:
        die( f'unknown option: {arg}' )

#---------------------------------------------------------
# Functions for interpolating tables in Aircraft.py
#---------------------------------------------------------
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
        if a < a0: a = a0 # die( f'interpolate() a={a} < a0={a0}' )
        f = (a - a0) / (a1 - a0)
        return lerp( f, b0, b1 )
    else:
        if a < a1: a = a1 # die( f'interpolate() a={a} < a0={a0}' )
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

def interpolate_closest_rows2( aa, a, table, b_col=1, a_col=0, a_modulo=0, ab_modulo=0 ):
    rr0 = find_closest_row( aa, table, -1 )
    rr1 = find_closest_row( aa, table, rr0 )
    aa0 = table[rr0][0]
    aa1 = table[rr1][0]
    bb0 = interpolate_closest_rows( a, table[rr0][1], b_col, a_col, a_modulo, ab_modulo )
    bb1 = interpolate_closest_rows( a, table[rr1][1], b_col, a_col, a_modulo, ab_modulo )
    return interpolate( aa, aa0, aa1, bb0, bb1, a_modulo, ab_modulo )

def interpolate_closest_rows3( aaa, aa, a, table, b_col=1, a_col=0, a_modulo=0, ab_modulo=0 ):
    rrr0 = find_closest_row( aaa, table, -1 )
    rrr1 = find_closest_row( aaa, table, rrr0 )
    aaa0 = table[rrr0][0]
    aaa1 = table[rrr1][0]
    bbb0 = interpolate_closest_rows2( aa, a, table[rrr0][1], b_col, a_col, a_modulo, ab_modulo )
    bbb1 = interpolate_closest_rows2( aa, a, table[rrr1][1], b_col, a_col, a_modulo, ab_modulo )
    return interpolate( aaa, aaa0, aaa1, bbb0, bbb1, a_modulo, ab_modulo )

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
# Compute Weight and Balance
#--------------------------------------------------------------
weight_for   = tail if tail_info else type
print()
print( f'Weight and Balance for {weight_for}' )
print()
total_weight = 0
total_moment = 0
empty_weight = tail_info['empty_weight'] if tail_info else type_info['empty_weight'] 
empty_arm    = tail_info['empty_arm']    if tail_info else type_info['empty_arm'] 
empty_moment = empty_weight * empty_arm
total_weight += empty_weight
total_moment += empty_moment
fuel_weight  = fuel_gal * type_info['fuel_gal_weight']
fuel_arm     = type_info['fuel_arm']
fuel_moment  = fuel_weight * fuel_arm
total_weight += fuel_weight
total_moment += fuel_moment
row1_arm     = type_info['row1_arm']
row1_moment  = row1_weight * row1_arm
total_weight += row1_weight
total_moment += row1_moment
row2_arm     = type_info['row2_arm']
row2_moment  = row2_weight * row2_arm
total_weight += row2_weight
total_moment += row2_moment
baggage1_arm     = type_info['baggage1_arm']
baggage1_moment  = baggage1_weight * baggage1_arm
baggage1_weight_max = type_info['baggage1_weight_max']
total_weight += baggage1_weight
total_moment += baggage1_moment
baggage2_arm     = type_info['baggage2_arm']
baggage2_moment  = baggage2_weight * baggage2_arm
baggage2_weight_max = type_info['baggage2_weight_max']
baggage_weight = baggage1_weight + baggage2_weight
baggage_weight_max = type_info['baggage_weight_max']
takeoff_weight_max = type_info['takeoff_weight_max']
total_weight += baggage2_weight
total_moment += baggage2_moment
total_arm = total_moment / total_weight
print( f'Item                      Weight    Arm     Moment' )
print( f'--------------------------------------------------' )
print( f'Empty Aircraft:           {empty_weight:6.1f} {empty_arm:6.2f}  {empty_moment:9.2f}' )
print( f'Main Fuel ({fuel_gal:2.0f} Gallons):   {fuel_weight:6.1f} {fuel_arm:6.2f}  {fuel_moment:9.2f}' )
print( f'Seating Row 1:            {row1_weight:6.1f} {row1_arm:6.2f}  {row1_moment:9.2f}' )
print( f'Seating Row 2:            {row2_weight:6.1f} {row2_arm:6.2f}  {row2_moment:9.2f}' )
print( f'Area 1 Baggage:           {baggage1_weight:6.1f} {baggage1_arm:6.2f}  {baggage1_moment:9.2f}' )
print( f'Area 2 Baggage:           {baggage2_weight:6.1f} {baggage2_arm:6.2f}  {baggage2_moment:9.2f}' )
print( f'--------------------------------------------------' )
print( f'Total:                    {total_weight:6.1f} {total_arm:6.2f}  {total_moment:9.2f}' )
print()

if baggage1_weight > baggage1_weight_max: print( f'PROBLEM: area 1 baggage weight ({baggage1_weight}) > max allowed ({baggage1_weight_max})' )
if baggage2_weight > baggage2_weight_max: print( f'PROBLEM: area 2 baggage weight ({baggage2_weight}) > max allowed ({baggage2_weight_max})' )
if baggage_weight  > baggage_weight_max:  print( f'PROBLEM: area 1+2 baggage weight ({baggage_weight}) > max allowed ({baggage_weight_max})' )
if total_weight <= takeoff_weight_max: 
    print( f'VERIFIED: takeoff weight ({total_weight}) <= max allowed ({takeoff_weight_max})' )
else:
    print( f'!!! PROBLEM: takeoff weight ({total_weight}) > max allowed ({takeoff_weight_max})' )
normal_cg_min = interpolate_closest_rows( total_weight, type_info['normal_cg'], 1 )
normal_cg_max = interpolate_closest_rows( total_weight, type_info['normal_cg'], 2 )
if total_arm >= normal_cg_min and total_arm <= normal_cg_max:
    pct = (total_arm-normal_cg_min) * 100.0 / (normal_cg_max - normal_cg_min)
    print( f'VERIFIED: takeoff CG ({total_arm:0.2f}) is {pct:.1f}% of normal range ({normal_cg_min:.2f} .. {normal_cg_max:.2f})' )
else:
    print( f'!!! PROBLEM: takeoff CG ({total_arm:0.2f}) is OUTSIDE normal range ({normal_cg_min:.2f} .. {normal_cg_max:.2f})' )
no_fuel_weight = total_weight - fuel_weight
no_fuel_moment = total_moment - fuel_moment
no_fuel_arm    = no_fuel_moment / no_fuel_weight
no_fuel_cg_min = interpolate_closest_rows( no_fuel_weight, type_info['normal_cg'], 1 )
no_fuel_cg_max = interpolate_closest_rows( no_fuel_weight, type_info['normal_cg'], 2 )
if no_fuel_arm >= no_fuel_cg_min and no_fuel_arm <= no_fuel_cg_max:
    pct = (no_fuel_arm-no_fuel_cg_min) * 100.0 / (no_fuel_cg_max - no_fuel_cg_min)
    print( f'VERIFIED: empty-fuel CG ({no_fuel_arm:0.2f}) is {pct:.1f}% of normal range ({no_fuel_cg_min:.2f} .. {no_fuel_cg_max:.2f})' )
else:
    print( f'!!! PROBLEM: empty-fuel CG ({no_fuel_arm:0.2f}) is OUTSIDE normal range ({no_fuel_cg_min:.2f} .. {no_fuel_cg_max:.2f})' )

#--------------------------------------------------------------
# Analyze Route and Compute NavLog
#--------------------------------------------------------------
MagVar.reinit()

# next 3 functions were transcribed from http://indoavis.co.id/main/tas.html Javascript code
# (they produce answers that are pretty close to my E6B app):
#
lapserate = 0.0019812		        # degrees / foot std. lapse rate C° in to K° result
tempcorr = 273.15			# Kelvin
stdtemp0 = 288.15			# Kelvin

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
    for i in range(len(table)>>1):
        if table[i*2+0] >= FLAPS:
            return interpolate_closest_rows( IAS, table[i*2+1] )
    die( f'flaps={FLAPS} has no relevant entry in the CAS table' )

def calc_DEV( MH, table ):
    return interpolate_closest_rows( MH, table, 1, 0, 360, 360 ) - MH

def reverse_route( rt ):
    rev = []
    for i in range(len(rt)):
        j = len(rt)-1-i
        rev.append( rt[j].copy() )
        rev[i]['ias'] = rt[i]['ias']                            # hack
        rev[i]['ia'] = rt[i]['ia']                              # hack  
        rev[i]['wind_dir'] = rt[i]['wind_dir']                  # hack  
        rev[i]['wind_speed'] = rt[i]['wind_speed']              # hack  
        rev[i]['oat'] = rt[i]['oat']                            # hack  
        rev[i]['fuel_gph'] = rt[i]['fuel_gph']                  # hack  
    id = rev[0]['id']
    if id in rawdata: rev[0]['ia'] = rawdata[id]['elevation']   # hack, but usually correct
    return rev

def calc_segment( fm, to ):
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
    TC   = (runway * 10) if i == 0 else Geodesic.initial_bearing( FM_LAT, FM_LON, TO_LAT, TO_LON )
    CAS  = calc_CAS( TO_IAS, TO_FLAPS, type_info['airspeed_calibration'] )
    WA   = TO_WD + 180
    while WA > 360: WA -= 360
    WTA  = TC - WA
    DIA  = TO_IA
    PA   = calc_PA( TO_IA, TO_ALT )
    DA   = calc_DA( PA, TO_OAT )
    TAS  = calc_TAS( CAS, DA )
    WCA  = RAD_TO_DEG*asin( TO_WS * sin( DEG_TO_RAD*WTA ) / TAS )
    TH   = TC + WCA
    MV   = (-MagVar.today_magvar( FM_LAT, FM_LON ) + -MagVar.today_magvar( TO_LAT, TO_LON )) / 2.0
    MH   = TH + MV
    DEV  = calc_DEV( MH, tail_info['magnetic_deviation'] ) if tail_info else 0
    CH   = MH + DEV
    GS   = TAS*cos( DEG_TO_RAD*WCA ) + TO_WS*cos( DEG_TO_RAD*WTA )
    ETE  = D/GS * 60.0
    GPH  = TO_GPH
    GAL  = (ETE / 60.0 * GPH) if i != 0 else fuel_gal_taxi

    return { 'TC': TC, 'CAS': CAS, 'TAS': TAS, 'WCA': WCA, 'TH': TH, 'MV': MV, 'MH': MH, 'DEV': DEV, 'CH': CH, 'D': D, 'GS': GS, 'ETE': ETE, 'GPH': GPH, 'GAL': GAL }

def route_analyze( rt ):
    global fuel_gal
    print()
    print()
    print( f'CHECKPOINT         LAT    LON  TC   IA   ALT  WD WS OAT   IAS CAS TAS   WCA  TH MV  MH DEV  CH       D  DTOT    GS   ETE   ETA      GPH  GAL  REM' )
    print( f'-------------------------------------------------------------------------------------------------------------------------------------------------' )
    DTOT = 0
    ETA = 0
    gal_rem = fuel_gal
    for i in range(len(rt)):
        fm = rt[0] if i == 0 else rt[i-1]
        to = rt[i]
        c = calc_segment( fm, to )

        TO_NAME = to['name']
        TO_LAT = to['lat']
        TO_LON = to['lon']
        TO_IAS = to['ias']
        TO_WS  = to['wind_speed']
        TO_WD  = to['wind_dir']
        TO_IA  = to['ia']
        TO_ALT = to['alt']
        TO_OAT = to['oat']
        TC     = c['TC']
        CAS    = c['CAS']
        TAS    = c['TAS']
        WCA    = c['WCA']
        TH     = c['TH']
        MV     = c['MV']
        MH     = c['MH']
        DEV    = c['DEV']
        CH     = c['CH']
        D      = c['D']
        GS     = c['GS']
        ETE    = c['ETE']
        GPH    = c['GPH']
        GAL    = c['GAL']

        DTOT += D
        ETA += ETE
        gal_rem -= GAL

        print( f'{TO_NAME:15s} {TO_LAT:6.2f} {TO_LON:6.2f} {TC:3.0f} {TO_IA:4.0f} {TO_ALT:5.2f} {TO_WD:3.0f} {TO_WS:2.0f} {TO_OAT:3.0f}   {TO_IAS:3.0f} {CAS:3.0f} {TAS:3.0f}   {WCA:3.0f} {TH:3.0f} {MV:2.0f} {MH:3.0f} {DEV:3.0f} {CH:3.0f}   {D:5.1f} {DTOT:5.1f} {GS:5.1f} {ETE:5.1f} {ETA:5.1f}     {GPH:4.1f} {GAL:4.1f} {gal_rem:4.1f}' )

    print()
    fuel_time_left_hr = gal_rem / fuel_gph
    fuel_time_left_min_hr = fuel_time_left_min / 60.0
    if fuel_time_left_hr >= fuel_time_left_min_hr:
        print( f'VERIFIED: fuel time left ({fuel_time_left_hr:0.2f} hr) >= minimum allowed ({fuel_time_left_min_hr:0.2f} hr)' )
    else:
        print( f'!!! PROBLEM: fuel time_left ({fuel_time_left_hr:0.2f} hr) < minimum allowed ({fuel_time_left_min_hr:0.2f} hr)' )

    if not fuel_refill: fuel_gal = gal_rem

route_analyze( route )
if show_return:
    return_route = reverse_route( route )
    route_analyze( return_route )

#--------------------------------------------------------------
# Print Short-Field Takeoff and Landing Distances
#--------------------------------------------------------------
print()
print()
print( f'Short-Field Takeoff and Landing Distances' )
print( f'-----------------------------------------' )
print()
fm = route[0]
FM_NAME = fm['name']
FM_ELE  = rawdata[FM_NAME]['elevation']
FM_ALT  = fm['alt']
FM_PA   = calc_PA( FM_ELE, FM_ALT )
FM_OAT  = fm['oat']
FM_ROLL    = interpolate_closest_rows3( total_weight, FM_OAT, FM_PA, type_info['short_field_takeoff'], b_col=1 )
FM_CLEAR50 = interpolate_closest_rows3( total_weight, FM_OAT, FM_PA, type_info['short_field_takeoff'], b_col=2 )
print( f'{FM_NAME} short-field TAKEOFF with {total_weight:.0f} lb, {FM_PA:.0f} ft pressure altitude (elevation={FM_ELE}, altimeter={FM_ALT}), and {FM_OAT}C' )
print( f'        ground roll:                           {FM_ROLL:5.0f} ft' )
print( f'        length to clear 50 ft obstacle:        {FM_CLEAR50:5.0f} ft' )
print()
to = route[len(route)-1]
TO_NAME = to['name']
TO_ELE  = rawdata[TO_NAME]['elevation']
TO_ALT  = to['alt']
TO_PA   = calc_PA( TO_ELE, TO_ALT )
TO_OAT  = to['oat']
TO_ROLL    = interpolate_closest_rows3( total_weight, TO_OAT, TO_PA, type_info['short_field_landing'], b_col=1 )
TO_CLEAR50 = interpolate_closest_rows3( total_weight, TO_OAT, TO_PA, type_info['short_field_landing'], b_col=2 )
print( f'{TO_NAME} short-field LANDING with {total_weight:.0f} lb, {TO_PA:.0f} ft pressure altitude (elevation={TO_ELE}, altimeter={TO_ALT}), and {TO_OAT}C' )
print( f'        ground roll:                           {TO_ROLL:5.0f} ft' )
print( f'        length to clear 50 ft obstacle:        {TO_CLEAR50:5.0f} ft' )

#--------------------------------------------------------------
# Print Useful Airport/Runway Information
#--------------------------------------------------------------
airports = {}
for i in range(len(route)):
    id = route[i]['id']
    if id != '': airports[id] = 1

#--------------------------------------------------------------
# Print Closest Diversions
#--------------------------------------------------------------
def runway_longest( runways ):
    best = None
    for runway in runways:
        if best == None or runway['length'] > best['length']: best = runway
    return best

print()
print()
print( f'Closest Diversions (with runway >= {runway_length_min} ft)' )
print( '-------------------------------------------' )
print()
checkpoints = []
#checkpoints.append(route[0].copy())
#checkpoints[0]['id'] = ''
#checkpoints[0]['name'] = ''
j = len(route) - 1
for i in range(len(route)):
    checkpoints.append(route[i].copy())
    if i != j: 
        for pct in [25, 50, 75]:
            name = f'  {pct}%'
            f = pct/100.0
            cp = route[i].copy()
            cp['id']  = ''
            cp['name'] = name
            cp['lat'] = lerp( f, route[i]['lat'], route[i+1]['lat'] )
            cp['lon'] = lerp( f, route[i]['lon'], route[i+1]['lon'] )
            checkpoints.append( cp )
#checkpoints.append(route[j].copy())
#j = len(checkpoints) - 1
#checkpoints[j]['id'] = ''
#checkpoints[j]['name'] = ''
diversions = [ {'id': '', 'D': 1e20, 'ETE': 1e20} for i in range(len(checkpoints)) ]
for did in rawdata:
    dtype = rawdata[did]['type']
    if dtype != 'AIRPORT': continue
    dname = rawdata[did]['name']
    dlat = rawdata[did]['lat']
    dlon = rawdata[did]['lon']
    delev = rawdata[did]['elevation']
    duse  = rawdata[did]['use']
    dunicom_freq = rawdata[did]['unicom_freq']
    dctaf_freq = rawdata[did]['ctaf_freq']
    drunways = rawdata[did]['runways']
    dlongest = runway_longest( drunways )
    if dlongest['length'] < runway_length_min: continue
    for i in range(len(checkpoints)):
        id = checkpoints[i]['id']
        if did != id:
            lat  = checkpoints[i]['lat']
            lon  = checkpoints[i]['lon']
            dist = Geodesic.distance( lat, lon, dlat, dlon )
            if dist < 200.0 and dist < (2*diversions[i]['D']):
                to = checkpoints[i].copy()
                to['lat'] = dlat
                to['lon'] = dlon
                c = calc_segment( checkpoints[i], to )
                D = c['D']
                if c['ETE'] < diversions[i]['ETE']:
                    c['id'] = did
                    c['name'] = dname
                    c['lat'] = dlat
                    c['lon'] = dlon
                    c['elevation'] = delev
                    c['use'] = duse
                    c['unicom_freq'] = dunicom_freq
                    c['ctaf_freq'] = dctaf_freq
                    c['runways'] = drunways
                    diversions[i] = c

print( f'Note: these diversions do not yet account for time required to turn to the diversion\'s compass heading (CH)' )
print()
print( f'CHECKPOINT         ICAO   CH    D  ETE ELEV PUBL    CTAF  LONGEST LENGTH WIDTH PATT   COND  NAME                           NEAR CITY' )
print( f'---------------------------------------------------------------------------------------------------------------------------------------------------------------' )
for i in range(len(checkpoints)):
    name = checkpoints[i]['name']
    did  = diversions[i]['id']
    dname= diversions[i]['name']
    dfrom_city = rawdata[did]['from_city'] if 'from_city' in rawdata[did] else ''
    CH   = diversions[i]['CH']
    D    = diversions[i]['D']
    ETE  = diversions[i]['ETE']
    elev = diversions[i]['elevation']
    public = 'Y' if diversions[i]['use'] == 'PU' else 'N'
    ctaf_freq = diversions[i]['ctaf_freq']
    unicom_freq = diversions[i]['unicom_freq']
    longest = runway_longest( diversions[i]['runways'] )
    runwayid  = longest['id']
    length    = longest['length']
    width     = longest['width']
    pattern   = 'R' if longest['pattern'] == 'Y' else 'L'
    pattern_rcp = 'R' if longest['pattern_rcp'] == 'Y' else 'L'
    pattern   = f'{pattern}/{pattern_rcp}'
    condition = longest['condition']
    print( f'{name:15s}    {did:4}  {CH:3.0f} {D:4.1f} {ETE:4.1f} {elev:4.0f}  {public:1s}   {ctaf_freq:7s}  {runwayid:7s}  {length:5.0f}  {width:4.0f}  {pattern} {condition:6s}  {dname:30s} {dfrom_city}' )

#--------------------------------------------------------------
# Print Airport Information
#--------------------------------------------------------------
print()
print()
print( 'Airport Information' )
print( '-------------------' )
airports = []
def add_airport( id ):
    if id == '': return
    if id not in rawdata: return
    for aid in airports:
        if id == aid: return    # already there
    airports.append( id )

morse_code_chars = { 'A':'.-', 'B':'-...',
                     'C':'-.-.', 'D':'-..', 'E':'.',
                     'F':'..-.', 'G':'--.', 'H':'....',
                     'I':'..', 'J':'.---', 'K':'-.-',
                     'L':'.-..', 'M':'--', 'N':'-.',
                     'O':'---', 'P':'.--.', 'Q':'--.-',
                     'R':'.-.', 'S':'...', 'T':'-',
                     'U':'..-', 'V':'...-', 'W':'.--',
                     'X':'-..-', 'Y':'-.--', 'Z':'--..',
                     '1':'.----', '2':'..---', '3':'...--',
                     '4':'....-', '5':'.....', '6':'-....',
                     '7':'--...', '8':'---..', '9':'----.',
                     '0':'-----', ', ':'--..--', '.':'.-.-.-',
                     '?':'..--..', '/':'-..-.', '-':'-....-',
                     '(':'-.--.', ')':'-.--.-'}

def get_morse_code( s ):
    su = s.upper()
    mc = ''
    for i in range(len(su)):
        if mc != '': mc += ' ' 
        c = su[i] 
        mc += morse_code_chars[c] if c in morse_code_chars else f'[{c}]' 
    return mc

for cp in checkpoints: add_airport( cp['id'] )
for al in alternate_airports: add_airport( al )
if show_diversion_detail: 
    for dv in diversions:  add_airport( dv['id'] )

for id in airports:
    print()
    #from_city = rawdata[id]['from_city'] if 'from_city' in rawdata[id] else ''
    #if from_city != '': from_city = f' ({from_city})' 
    #print( f'{id}{from_city}:' )
    print( f'{id}:' )
    name= rawdata[id]['name']
    from_city = rawdata[id]['from_city'] if 'from_city' in rawdata[id] else ''
    print( f'    NAME       {name:25s} {from_city}' )
    elev = rawdata[id]['elevation']
    print( f'    ELEVATION                            {elev}' )
    for r in rawdata[id]['runways']:
        # {'site': '16756.3*A', 'id': '09/27', 'length': 2400, 'width': 30, 'condition': 'ASPH-F', 'pattern': '', 'pattern_rcp': 'N'}
        rid = r['id']
        l = r['length']
        w = r['width']
        lxw = f'{l} x {w}'
        cond = r['condition']
        pattern   = 'R' if longest['pattern'] == 'Y' else 'L'
        pattern_rcp = 'R' if longest['pattern_rcp'] == 'Y' else 'L'
        pattern   = f'{pattern}/{pattern_rcp}'
        print( f'    RUNWAY     {rid:10s}                {lxw:12}    {pattern:3}        {cond:10s}' )
    for f in rawdata[id]['freqs']:
        freq = f['freq']
        if freq == '' or freq[0] != '1': continue
        kind = f['kind']
        remarks = f['remarks']
        if 'telephone' in f: remarks = f['telephone'] + '  ' + remarks
        print( f'    {kind:36s} {freq:15s} {remarks}' )
    for n in rawdata[id]['navaids']:
        freq = n['freq']
        if freq == '' or freq[0] != '1': continue
        kind = n['kind']
        if kind != 'VOR' and kind != 'VORTAC' and kind != 'VOR/DME' and kind != 'TACAN': continue
        nid = n['id']
        name = n['name']
        dist = n['distance']
        bearing = n['bearing']
        remarks = n['remarks']
        mc = get_morse_code( nid )
        print( f'    {kind:10s} {nid:4} {name:20s} {freq:15s} {dist:10s} FROM {bearing:8s} {mc:15s} {remarks}' )
