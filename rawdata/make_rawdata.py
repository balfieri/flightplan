#!/usr/local/bin/python3
#
# make_rawdata.py
#
# Downloads various interesting data files from the internet and extracts information needed by ../fp.py and stores
# it into a file called rawdata.dat which is saved in the repository occasionally.   
#
import os
import subprocess
import time
import csv
import pickle
import re

def die( msg ):
    print( f'ERROR: {msg}' )
    sys.exit( 1 )

cmd_en = True

def cmd( c ):  
    print( c )
    if cmd_en:
        info = subprocess.run( c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        if info.returncode != 0: die( f'command failed: {c}' )
        return info.stdout
    else:
        return ''

m = None 
def match( s, pattern ): 
    global m
    m = re.compile( pattern ).match( s )
    return m

def subst( s, pattern, subst ):
    return re.sub( pattern, subst, s )

rawdata = {}

def download():
    # TODO: we currently manually download the files
    cmd( 'mkdir -p airports' )
    pass

def latlon_to_decimal( latlon ):
    ch = latlon[-1:]
    latlon = float(latlon[:-1]) / 3600.0
    if ch == 'S' or ch == 'W': latlon = -latlon
    return latlon

def parse_faa_text( id ):
    #--------------------------------------------------------------
    # Download more detailed information from faa.gov, but don't 
    # do this if we have alread done it for a particular airport.
    # Convert html to text and write to the .faa.text.out file.
    #--------------------------------------------------------------
    if not os.path.exists( f'airports/{id}.faa.out' ):
        for t in range(10):
            time.sleep( 1 )
            c = f'wget -O - https://nfdc.faa.gov/nfdcApps/services/ajv5/airportDisplay.jsp?airportId={id} > airports/{id}.faa.out'
            print( c )
            info = subprocess.run( c, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
            if info.returncode == 0: break
            cmd( f'rm -f airports/{id}.faa.out' )
            if t == 9: print( f'could not get FAA airport data for {id}' )
    if os.path.exists( f'airports/{id}.faa.out' ) and not os.path.exists( f'airports/{id}.faa.text.out' ):
        cmd( f'html2text airports/{id}.faa.out > airports/{id}.faa.text.out' )

    #--------------------------------------------------------------
    # Parse the more detailed faa.text.data information that is not
    # available in the .csv files and insert it back into 
    # the rawdata for this airport.  
    #--------------------------------------------------------------
    info = rawdata[id]
    info['freqs'] = []
    info['navaids'] = []
    if not os.path.exists( f'airports/{id}.faa.text.out' ): return

    T = open( f'airports/{id}.faa.text.out' )
    multi_freqs_kind = ''
    while True:
        line = T.readline()
        if line == '': break

        if multi_freqs_kind != '' and match( line, r'^\s+\|\s*(\S.*\S)\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)?' ):
            info['freqs'].append( { 'kind': multi_freqs_kind, 'freq': m.group(1), 'subkind': m.group(2), 'remark': m.group(3) } )
            continue
        multi_freqs_kind = ''

        if match( line, r'^(UNICOM|CTAF|ATIS):\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)?' ):
            freq = m.group(2) 
            if freq == 'None': freq = ''
            remarks = m.group(3)
            if not remarks: remarks = ''
            info['freqs'].append( { 'kind': m.group(1), 'freq': freq, 'remarks': remarks } )
        elif match( line, r'^(\S.*\S) (APPROACH|DEPARTURE|DELIVERY|GROUND|TOWER):\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)?' ):
            multi_freqs_kind = m.group( 1 ) + ' ' + m.group( 2 )
            remarks = m.group(5)
            if not remarks: remarks = ''
            info['freqs'].append( { 'kind': multi_freqs_kind, 'freq': m.group(3), 'subkind': m.group(4), 'remarks': remarks } )
        elif match( line, r'^(DME|NDB|VOR/DME|VORTAC|TACAN)\s*\|\s*(\w+)\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)\s*\|\s*(\S.*\S)?' ):
            remarks = m.group(8)
            if not remarks: remarks = ''
            info['navaids'].append( { 'kind': m.group(1), 'id': m.group(2), 'name': m.group(3), 'freq': m.group(4), 'hours': m.group(5), 
                                      'distance': m.group(6), 'bearing': m.group(7), 'remarks': remarks } )

    T.close()

def read():
    print( f'Reading NfdcRunways.csv...' )
    runways = {}                
    with open( 'NfdcRunways.csv', 'r' ) as csv_file:
        reader = csv.reader( csv_file )
        have_one = False
        for row in reader:
            if not have_one:
                # skip first line
                have_one = True
                continue
            site = row[0]
            runway = { 'site':          site,
                       'id':            re.sub( r'\'', '', row[2] ),
                       'length':        int(row[3]),
                       'width':         int(row[4]),
                       'condition':     row[5],
                       'pattern':       row[12],
                       'pattern_rcp':   row[46]}
            if site not in runways: runways[site] = []
            runways[site].append( runway )
        csv_file.close()

    print( f'Reading NfdcFacilities.csv...' )
    with open( 'NfdcFacilities.csv', 'r' ) as csv_file:
        reader = csv.reader( csv_file )
        have_one = False
        for row in reader:
            #--------------------------------------------------------------
            # Get airport information that's available from these .csv files.
            #--------------------------------------------------------------
            if not have_one:
                # skip first line
                have_one = True
                continue
            id = row[len(row)-2]
            if id == '': id = row[2].replace( "'", "" )

            rawdata[id] = { 'site':      row[0],
                            'type':      row[1],
                            'state':     row[6],
                            'city':      row[10],
                            'name':      row[11],
                            'use':       row[13],
                            'lat':       latlon_to_decimal( row[23] ),
                            'lon':       latlon_to_decimal( row[25] ),
                            'elevation': int(row[27]),
                            'unicom_freq': row[73],
                            'ctaf_freq': row[74],
                            'runways':   runways[row[0]] if row[0] in runways else [] }

            #--------------------------------------------------------------
            # Download and parse more detailed information from faa.gov.
            #--------------------------------------------------------------
            parse_faa_text( id )

        csv_file.close()

def write():
    print( f'Writing {len(rawdata)} entries to rawdata.dat...' )
    print( rawdata['KTTA'] )
    out = open( 'rawdata.dat', 'wb' )
    pickle.dump( rawdata, out )
    out.close()


download()
read()
write()
