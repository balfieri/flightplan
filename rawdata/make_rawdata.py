#!/usr/local/bin/python3
#
# make_rawdata.py
#
# Downloads various interesting data files from the internet and extracts information needed by ../fp.py and stores
# it into a file called rawdata.dat which is saved in the repository occasionally.   
#
import csv
import pickle

rawdata = {}

def download():
    # TODO: we currently manually download the files
    pass

def latlon_to_decimal( latlon ):
    ch = latlon[-1:]
    latlon = float(latlon[:-1]) / 3600.0
    if ch == 'S' or ch == 'W': latlon = -latlon
    return latlon

def read():
    print( f'Reading NfdcFacilities.csv...' )
    with open( 'NfdcFacilities.csv', 'r' ) as csv_file:
        reader = csv.reader( csv_file )
        have_one = False
        for row in reader:
            if not have_one:
                # skip first line
                have_one = True
                continue
            id = row[len(row)-2]
            if id == '': id = row[2].replace( "'", "" )
            rawdata[id] = { 'site':     row[0],
                            'type ':    row[1],
                            'state':    row[6],
                            'city':     row[10],
                            'name':     row[11],
                            'lat':      latlon_to_decimal( row[23] ),
                            'lon':      latlon_to_decimal( row[25] ) }
            
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
