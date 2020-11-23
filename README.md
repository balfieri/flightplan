This repository contains a Python3 script that can create a textual flight plan from a set of checkpoints.  


CURRENT FEATURES<br>
----------------

It shows the textual flight plan in a compact navlog format that should be familiar to most pilots.  It performs table lookups for CAS, MV, and DEV.  The flight plan is still somewhat manual. The user must provide average IAS, IA (indicated altitude), WD (wind direction), WS (wind speed), etc. values for each leg.  It verifies that fuel time left is more than allowed (default: one hour).

It prints out a weight-and-balance check for the specific tail number and type.

It prints out the closest diversion airport information (default: with a runway >= 2000 ft) for each checkpoint 
as well as for 25%, 50%, and 75% midpoints between checkpoints.

It prints out information for all airports such as runways, comm frequencies, and navaids.

FUTURE FEATURES<br>
---------------

It will compute required takeoff roll and verify that the takeoff runway supports it.  Similar for landing.

It will look up METARs, TAFs, winds aloft, PIREPs, SIGMETs, AIRMETs, etc. from aviationweather.gov.

It will consult obstacle and terrain-elevation databases and print out closest hazards along the route.

It will compute optimal cruising altitude for each leg of the flight.

It will compute a more accurate piecewise integration of each leg. In other words, do minute-by-minute computations and derive integrated GS and fuel consumption along the way.  It will also attempt to emulate takeoff, descent, and landing more accurately, including time departing the pattern and getting back onto the proper course (and opposite for landing).

It will run in-flight on a phone/iPad (using the Pyto app) and monitor the phone/iPad's GPS location. This allows it to give you simple alerts when you are reaching checkpoints, deviating from them, deviating from planned altitude, exceeding planned fuel burn, needing to start descending, or getting close to terrain or obstacles.  Further, it will show the heading and distance to the nearest airport and whether you are within gliding distance. 

WARNING: The in-flight functionality will NOT be a replacement for an onboard navigation system! It is for situational awareness and having a compact representation of data.  You should use this in conjunction with other REDUNDANT mechanisms such as the CERTIFIED onboard navigation and traffic monitoring system, looking out the window (duh!), having a copilot/helper, ATC flight following, and Foreflight + iPad + Stratus/Stratux.

The program is divided into the following files:
  
    fp.py               -- the main program
    Aircraft.py         -- performance characteristics of various types of aircraft and 
                           overrides for specific tail numbers (feel free to augment this file)
    Geodesic.py         -- computes great-circle distance and course 
                           between any two points on Earth (and related things)
    MagVar.py           -- computes magnetic variation at any point on Earth for a given date
    rawdata/            -- airport/waypoint GPS coordinates and facility/runway information
                           that is filtered down by a script called rawdata/make_rawdata.py 
                           and written to a checked-in pickle-format file called 
                           rawdata/rawdata.dat that is easily sucked in by fp.py

Example run scripts:

    doit.kbuy_kclt      -- KBUY to KCLT with checkpoints 
    doit.ktta_kgso      -- KTTA to KGSO with checkpoints
    doit.kgso_ktta      -- KGSO to KTTA with checkpoints

This is all open-source.  Refer to the LICENSE.md for licensing details.  

Bob Alfieri<br>
Chapel Hill, NC
