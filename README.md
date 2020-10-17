NOTE: this is a work-in-progress, most of these features are fully functional yet

This repository contains a Python3 script that can create a textual flight plan from a set of checkpoints.  The textual flight plan is compact and can be printed on a single sheet of paper in a navlog format that should be familiar to most pilots.  The script shows other information such as radio frequencies, runways, and FBOs.

The script can also run in-flight on a phone/iPad (using the Pyto app) and monitor the phone/iPad's GPS location. This allows it to give you simple alerts when you are reaching checkpoints, deviating from them, deviating from planned altitude, exceeding planned fuel burn, needing to start descending, or getting close to terrain or obstacles.  Further, It will show the heading and distance to the nearest airport and whether you are within gliding distance. 

WARNING: This is NOT a replacement for an onboard navigation system! This is more about situational awareness and having a compact representation of data.  You should use this in conjunction with other REDUNDANT mechanisms such as the certified onboard navigation and traffic monitoring system, looking out the window (duh!), having a copilot/helper, ATC flight following, and Foreflight + iPad + Stratus/Stratux.

The program is divided into the following files:
  
    fp.py               -- the main program
    Aircraft.py         -- performance characteristics of various types of aircraft and 
                           overrides for specific tail numbers (feel free to augment this file)
    Geodisic.py         -- computes great-circle distance and course 
                           between any two points on earth (and related things)
    MagVar.py           -- computes magnetic variation at any point on Earth for a given date

I will show run lines later once this is done.

This is all open-source.  Refer to the LICENSE.md for licensing details.  

Bob Alfieri
Chapel Hill, NC
