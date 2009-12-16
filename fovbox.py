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

# option parser (see http://docs.python.org/library/optparse.html)
usage = "Usage: %prog [options] longitude latitude field_of_view_x [field_of_view_y]"
parser = OptionParser(usage)
parser.add_option("-o", "--output", dest="output", help="[dd (default) | dms] -- dd is decimal degrees ([-]123.1234), dms is degrees-minutes-seconds (dd:mm:ss[NSEW]")
(options, args) = parser.parse_args()
if not options.output:
    options.output = 'dd'
if options.output and options.output.lower() not in ['dd', 'dms', None]:
    parser.error("Invalid option for input: %s" % options.input)

print args
print options

def _main():
    """Main"""
    
    print "hello world"
    
    return 0

if __name__ == "__main__":
    _main()
