This repository contains a Python script that can create a textual flight plan from a set of way points.  The textual flight plan is compact and can be printed on a single sheet of paper in the same format that my flight club uses, then printed off and placed on my kneeboard.  The script can also run on a phone (using the Pyto app) and can monitor GPS location in-flight.  It can then give you simple alerts when you are reaching way points, deviating from them, deviating from planned altitude, deviate from planned fuel burn, need to start descending, or should be made aware of a nearby aircraft or obstacle.

This is NOT a replacement for an onboard navigation system!

The intention is to assist in flight planning and to act as another eyeball for in-flight situational awareness.  It's like a poor man's Foreflight that has been scaled down and optimized to perform the kinds of tasks that I feel are important to me and in the format that I prefer to look at them.  I use this in conjunction with other mechanisms such as looking out the window(!), having a copilot/helper, 
ATC flight following, Foreflight+iPad+Stratux, and obviously the onboard navigation system.

The program is divided into the following files:
* fp.py - the main program
* Aircraft.py - performance characteristics of various types of aircraft and overrides for specific tail numbers
* Geodisic.py - computes great-circle distance and course between any two points on earth (among other things)
* MagneticVariation.py - computes magnetic variation at any point on earth

I will show run lines later once this is done.
