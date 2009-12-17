#!/usr/bin/env python
"""
fovbox can parse any of these coordinate representations:


"""

import sys
import math
from optparse import OptionParser

from coordinate import Coordinate

# global variables
center_point = 0
left_coord = 0
bottom_coord = 0
right_coord = 0
top_coord = 0

# debug
DEBUG = True

# option parser (see http://docs.python.org/library/optparse.html)
usage = "Usage: %prog [options] longitude latitude altitude field_of_view_x [field_of_view_y]"
parser = OptionParser(usage)
parser.add_option("-o", "--output", dest="output", help="[dd (default) | dms] -- dd is decimal degrees ([-]123.1234); dms is degrees-minutes-seconds (11d 22m 33.333s [NSEW]).")
parser.add_option("-u", "--units", dest="units", help="[m (default] | km | ft | mi] -- Units of altitude. m is meters; km is kilometers; ft is feet; mi is miles.")
parser.add_option("-a", "--angle", dest="angle", help="[d (default) | r] -- Units of the field of view angle. d is degrees; r is radians.")

(options, args) = parser.parse_args()

if not options.output:
    options.output = 'dd'
if options.output.lower() not in ['dd', 'dms']:
    parser.error("Invalid option for input: %s" % options.input)

if not options.units:
    options.units = 'm'
if options.units.lower() not in ['m', 'km', 'ft', 'mi']:
    parser.error("Invalid option for units: %s" % options.units)

if not options.angle:
    options.angle = 'd'
if options.angle.lower() not in ['d', 'r']:
    parser.error("Invalid option for angle: %s" % options.angle)

options.output = options.output.lower()
options.units = options.units.lower()
options.angle = options.angle.lower()

if len(args) < 4:
    parser.error("Not enough arguments.")
if len(args) > 5:
    parser.error("Too many arguments.")

if DEBUG:
    print args
    print options

def _main():
    """Main"""
    
    global DEBUG, parser, options, args
    
    lon = Coordinate(args[0], "Lon")
    lat = Coordinate(args[1], "Lat")
    
    if not lon.isValid():
        parser.error("Invalid longitudinal coordinate: %s" % lon.getCoord())
    if not lat.isValid():
        parser.error("Invalid latitudinal coordinate: %s" % lat.getCoord())
    
    return 0

if __name__ == "__main__":
    _main()
