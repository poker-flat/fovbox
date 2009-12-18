#!/usr/bin/env python
"""
fovbox can parse any of these coordinate representations:


"""

import sys
import math
from optparse import OptionParser

from coordinate import Coordinate
from coordinate import Point

__VERSION__ = "0.1"

# global variables
center_point = 0
left_coord = 0
bottom_coord = 0
right_coord = 0
top_coord = 0

# debug
DEBUG = False

# factor to convert degrees to radians (PI/180) and radians to degrees.
DEG2RAD =  0.01745329252
RAD2DEG = 57.29577951308

# option parser (see http://docs.python.org/library/optparse.html)
usage = "%prog [options]"
parser = OptionParser(usage=usage, version="%prog "+__VERSION__)
parser.add_option("--lon", "--longitude", dest="lon", help="REQUIRED. Geographic coordinate for the Longitude.")
parser.add_option("--lat", "--latitude", dest="lat", help="REQUIRED. Geographic coordinate for the Latitude.")
parser.add_option("--alt", "--altitude", dest="alt", help="REQUIRED. Altitude from the earth.")
parser.add_option("--fov", dest="fov", help="REQUIRED. Field of view. 0 < fov < 180 degrees; 0 < fov < %s radians." % math.pi)
parser.add_option("--fovx", dest="fovx", help="If FOV is not passed in, this is REQUIRED. Field of view in X. 0 < fov < 180 degrees; 0 < fov < %s radians." % math.pi)
parser.add_option("--fovy", dest="fovy", help="If FOV is not passed in, this is REQUIRED. Field of view in Y. 0 < fov < 180 degrees; 0 < fov < %s radians." % math.pi)
parser.add_option("-o", "--output", dest="output", help="[dd (default) | dms] -- dd is decimal degrees ([-]123.1234); dms is degrees-minutes-seconds (11d 22m 33.333s [NSEW]).")
parser.add_option("-u", "--units", dest="units", help="[m (default) | km | ft | mi] -- Units of altitude. m is meters; km is kilometers; ft is feet; mi is miles.")
parser.add_option("-a", "--angle", dest="angle", help="[d (default) | r] -- Units of the field of view angle. d is degrees; r is radians.")

(options, args) = parser.parse_args()

# Parse arguments
if options.lon == None:
    parser.error("Must pass in the --lon option.")

if options.lat == None:
    parser.error("Must pass in the --lat option.")

if options.alt == None:
    parser.error("Must pass in the --alt option.")

if options.fovx != None and options.fovy == None:
    parser.error("Must pass in the --fovy option.")

if options.fovy != None and options.fovx == None:
    parser.error("Must pass in the --fovx option.")

if options.fov == None and not (options.fovx != None and options.fovy != None):
    parser.error("Must pass in the --fov option.")

lon = Coordinate(options.lon, "Lon")
lat = Coordinate(options.lat, "Lat")

if not lon.isValid():
    parser.error("Invalid longitudinal coordinate: %s" % lon.getCoord())
if not lat.isValid():
    parser.error("Invalid latitudinal coordinate: %s" % lat.getCoord())

# Center point
cp = Point(options.lon, options.lat)

try:
    alt = float(options.alt)
except:
    parser.error("Invalid altitude: %s. Altitude must be a number." % options.alt)

if options.fov == None:
    try:
        fov_x = float(options.fovx)
    except:
        parser.error("Invalid field of view in X: %s. Field of view must be a number." % options.fovx)
    
    try:
        fov_y = float(options.fovy)
    except:
        parser.error("Invalid field of view in Y: %s. Field of view must be a number." % options.fovy)
else:
    try:
        fov_x = float(options.fov)
        fov_y = float(options.fov)
        options.fovx = options.fov
        options.fovy = options.fov
    except:
        parser.error("Invalid field of view: %s. Field of view must be a number." % options.fov)

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

if alt < 0:
    parser.error("Invalid altitude: %s. Altitude cannot be negative." % alt)

if fov_x <= 0:
    parser.error("Invalid field of view in X: %s. Field of view cannot be negative or zero." % fov_x)

if options.angle == 'd' and fov_x >= 180.0:
    parser.error("Invalid field of view in X: %s. Field of view must be less than 180.0" % fov_x)

if options.angle == 'r' and fov_x >= math.pi:
    parser.error("Invalid field of view in X: %s. Field of view must be lass than %s" % (fov_x, math.pi))

if fov_y <= 0:
    parser.error("Invalid field of view in Y: %s. Field of view cannot be negative or zero." % fov_y)

if options.angle == 'd' and fov_y >= 180.0:
    parser.error("Invalid field of view in Y: %s. Field of view must be less than 180.0" % fov_y)

if options.angle == 'r' and fov_y >= math.pi:
    parser.error("Invalid field of view in Y: %s. Field of view must be lass than %s" % (fov_y, math.pi))

if options.angle == 'd' and (cp.x < -180.0 or cp.x > 180.0):
    parser.error("Invalid longitudinal coordinate: %s. Longitude must be between -180.0 and 180 degrees." % cp.x)

if options.angle == 'd' and (cp.y < -90.0 or cp.y > 90.0):
    parser.error("Invalid latitudinal coordinate: %s. Latitude must be between -90.0 and 180.0 degrees." % cp.y)

if options.angle == 'r' and (cp.x < 0 or cp.x > math.pi):
    parser.error("Invalid longitudinal coordinate: %s. Longitude must be between 0 and %s radians." % (cp.x, math.pi))

if options.angle == 'r' and (cp.y < 0 or cp.y > (math.pi/2.0)):
    parser.error("Invalid latitudinal coordinate: %s. Latitude must be between 0 and %s radians." % (cp.y, (math.pi/2.0)))

if DEBUG:
    print options

xhalf = fov_x/2.0
yhalf = fov_y/2.0

if options.angle == 'd':
    fov_x = fov_x * DEG2RAD
    fov_y = fov_y * DEG2RAD

# Calculate the top and bottom edge of the viewing angle
d_vert = alt * math.tan( fov_y )

# Calculate the left and right edge of the viewing angle
d_horiz = alt * math.tan( fov_x )

# Convert radians to degrees
d_vert = d_vert * RAD2DEG
d_horiz = d_horiz * RAD2DEG

# Calculate corner distance
dist = math.sqrt( d_vert * d_vert + d_horiz * d_horiz )

# upper plane (only use the y value)
upper = cp.geoWaypoint(d_vert, 0.0, options.units)

# lower plane (only use the y value)
lower = cp.geoWaypoint(d_vert, 180.0, options.units)

# left plane (only use the x value)
left = cp.geoWaypoint(d_horiz, 270.0, options.units)

# right plane (only use the x value)
right = cp.geoWaypoint(d_horiz, 90.0, options.units)

# upper left point
ul = Point(left.x, upper.y)

# upper right point
ur = Point(right.x, upper.y)

# lower right point
lr = Point(right.x, lower.y)

# lower left point
ll = Point(left.x, lower.y)

print "UL    %s" % ul
print "LL    %s" % ll
print "UR    %s" % ur
print "LR    %s" % lr
print "CP    %s" % cp

print "Distance: %s %s" % (dist, options.units)

print "Upper left distance from center point: %s %s" % (cp.geoDistanceTo(ul, options.units), options.units)


