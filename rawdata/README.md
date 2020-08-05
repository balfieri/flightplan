This folder contains a script called make_rawdata.py that downloads interesting airport, waypoint, etc. data from FAA and other sites.  
It then extracts pieces of data that we care about and puts the in a Python data structure keyed by airport/waypoint code (e.g., KTTA)
and uses the pickle package to write that data structure to a file called rawdata.dat.

../fp.py uses pickle to then read in rawdata.dat.

rawdata.dat is checked into the repository, so you need not run make_rawdata.py yourself unless you want to make
sure you have the most up-to-date information.
