This repository contains a Python3 script that can create a textual flight plan from a set of checkpoints.  


CURRENT FEATURES<br>
----------------

The textual flight plan is compact and can be printed on a single sheet of paper in a navlog format that should be familiar to most pilots.  It performs table lookups for CAS, MV, and DEV.  The flight plan is still somewhat manual. The user must provide average IAS, IA (indicated altitude), WD (wind direction), WS (wind speed), etc. values for each leg. 

The script prints out elevations for all airports mentioned in the route.

FUTURE FEATURES<br>
---------------

The script will look up and show other information such as radio frequencies, runways, and FBOs.

The script will look up winds aloft information from online weather databases.

The script will compute a weight-and-balance for the specific tail number and type.

The script will compute a near-perfect piecewise integration of each leg. In other words, do minute-by-minute computations and derive integrated GS and fuel consumption along the way.  It will also attempt to emulate takeoff, descent, and landing more accurately, including time departing the pattern and getting back onto the proper course (and opposite for landing).

The script will run in-flight on a phone/iPad (using the Pyto app) and monitor the phone/iPad's GPS location. This allows it to give you simple alerts when you are reaching checkpoints, deviating from them, deviating from planned altitude, exceeding planned fuel burn, needing to start descending, or getting close to terrain or obstacles.  Further, It will show the heading and distance to the nearest airport and whether you are within gliding distance. 

WARNING: The in-flight functionality will NOT be a replacement for an onboard navigation system! It is for situational awareness and having a compact representation of data.  You should use this in conjunction with other REDUNDANT mechanisms such as the CERTIFIED onboard navigation and traffic monitoring system, looking out the window (duh!), having a copilot/helper, ATC flight following, and Foreflight + iPad + Stratus/Stratux.

The program is divided into the following files:
  
    fp.py               -- the main program
    Aircraft.py         -- performance characteristics of various types of aircraft and 
                           overrides for specific tail numbers (feel free to augment this file)
    Geodesic.py         -- computes great-circle distance and course 
                           between any two points on Earth (and related things)
    MagVar.py           -- computes magnetic variation at any point on Earth for a given date

Example run scripts:

    doit.kbuy_kclt      -- KBUY to KCLT with checkpoints 
    doit.ktta_kgso      -- KTTA to KGSO with checkpoints
    doit.kgso_ktta      -- KGSO to KTTA with checkpoints

This is all open-source.  Refer to the LICENSE.md for licensing details.  

Bob Alfieri<br>
Chapel Hill, NC
