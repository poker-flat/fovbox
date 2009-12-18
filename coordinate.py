"""
Module: coordinate

Description:
Coordinate library that contains these classes:
{<Coordinate>} - Parses and represents geographic coordinates (latitude and
                 longitude).
{<Point>} - Contains methods to calculate range, bearing, and create points
            from those.

Decimal degrees:
    123.12341234[NSEW]
    [NSEW+-]123.12341234
    
Degrees-minutes-seconds:
    [NSEW+-]11d 22m 33.33333s
    11d 22m 33.33333s[NSEW]
    11:22:33.33333[NSEW]
    [NSEW+-]11:22:33.33333
    
Examples:
    -64.12347874
    44D 10M 32.123S S
    N 89.1234
"""

import re
import math

EARTH_RADIUS_MI = 3958.761   # in miles (According to IUGG)
EARTH_RADIUS_FT = EARTH_RADIUS_MI * 5280.0
EARTH_RADIUS_KM = 6371.009   # in kilometers (According to IUGG)
EARTH_RADIUS_M = EARTH_RADIUS_KM * 1000.0
EARTH_RADIUS_NMI = 3440.069  # in nautical miles (According to IUGG).
EARTH_RADIUS = EARTH_RADIUS_KM # default radius
DEG2RAD =  0.01745329252  # factor to convert degrees to radians (PI/180)
RAD2DEG = 57.29577951308

class Coordinate:
    """
    Class: Coordinate
    
    Description:
    Parse an input into a known coordinate.
    """
    
    coord = None     # string
    
    coord_dd = None  # real number
    coord_dms = None # 3-tuple
    direction = None # string in [N,S,E,W]
    
    groups = None    # tuple
    
    # NOTE: Order Matters. The first two produce a 4-tuple, the other four
    # produce a 6-tuple
    regs = [
        # 123.12341234[NSEW]
        re.compile(r'''^\s*()([0-9]{0,3}(\.[0-9]{1,15})?)\s*([nNsSeEwW]?)\s*$'''),
        
        # [NSEW+-]123.12341234
        re.compile(r'''^\s*([nNsSeEwW+-]?)\s*([0-9]{0,3}(\.[0-9]{1,15})?)()\s*$'''),
        
        # [NSEW+-]11d22m33.333333s
        re.compile(r'''\s*([nNsSeEwW+-]?)\s*([0-9]{0,3})\s*[dD]\s*([0-9]{0,2})\s*[mM]\s*([0-9]{0,2}(\.[0-9]{1,15})?)\s*[sS]()\s*$'''),
        
        # 11d22m33.333333s[NSEW]
        re.compile(r'''\s*()([0-9]{0,3})\s*[dD]\s*([0-9]{0,2})\s*[mM]\s*([0-9]{0,2}(\.[0-9]{1,15})?)\s*[sS]\s*([nNsSeEwW]?)\s*$'''),
        
        # [NSEW+-]11:22:33.333333
        re.compile(r'''\s*([nNsSeEwW+-]?)\s*([0-9]{0,3})\s*:\s*([0-9]{0,2})\s*:\s*([0-9]{0,2}(\.[0-9]{1,15})?)()\s*$'''),
        
        # 11:22:33.333333[NSEW]
        re.compile(r'''\s*()([0-9]{0,3})\s*:\s*([0-9]{0,2})\s*:\s*([0-9]{0,2}(\.[0-9]{1,15})?)\s*([nNsSeEwW]?)\s*$'''),
        
        ]
    
    
    def __init__(self, coord, axis=''):
        """
        Constructor: __init__
        
        Parameters:]
        coord - {string} The unformatted coordinate to parse
        axis  - {string} The axis in which the unformatted coordinate is in.
                         Either Longitude or Latitude.
        """
        
        self.coord = str(coord)
        self._parse(axis)
    
    
    def _parse(self, axis=''):
        """
        Private Method: _parse
        
        Parameters:
        axis - {string} The axis in which the unformatted coordinate is in.
                        Either Longitude or Latitude
        """
        
        # Match the unformatted coordinate by the given regular expressions
        # list.
        position = 1
        for r in self.regs:
            m = r.match(self.coord)
            if m:
                self.groups = m.groups()
                break
            else:
                position += 1
                continue
        
        # If there was no match, return.
        if not self.groups:
            return
        
        # Parse direction and coordinate.
        if position <= 2:
            if self.groups[0]:
                self._parse_direction(self.groups[0], axis)
            elif self.groups[3]:
                self._parse_direction(self.groups[3], axis)
            else:
                self._parse_direction("+", axis)
            self._parse_dd(self.groups[1])
        elif position <= 6:
            if self.groups[0]:
                self._parse_direction(self.groups[0], axis)
            elif self.groups[5]:
                self._parse_direction(self.groups[5], axis)
            else:
                self._parse_direction("+", axis)
            self._parse_dms((self.groups[1], self.groups[2], self.groups[3]))
    
    
    def _parse_direction(self, direction, axis):
        """
        Private Method: _parse_direction
        
        Parameters:
        direction - {string} The direction, given by a string of either +, -, N,
                             S, E, or W.
        axis - {string} The axis in which the unformatted coordinate is in.
                        Either Longitude or Latitude.
        """
        
        direction = direction.lower()
        axis = axis.lower()
        
        if direction in ['n', 's', 'e', 'w']:
            self.direction = direction.upper()
            return
        
        if axis in ['latitude', 'lat']:
            if direction == '+' or direction == '':
                self.direction = 'N'
            else:
                self.direction = 'S'
        elif axis in ['longitude', 'lon', 'long']:
            if direction == '+' or direction == '':
                self.direction = 'E'
            else:
                self.direction = 'W'
        else:
            if direction == '+' or direction == '':
                self.direction = 'N'
            else:
                self.direction = 'S'
    
    
    def _parse_dms(self, dms):
        """
        Private Method: _parse_dms
        
        Parameters:
        dms - {3-tuple} A 3-tuple representing the degrees, minutes, and seconds
                        of a coordinate.
        """
        
        if len(dms) != 3 or not isinstance(dms, tuple):
            return
        
        self.coord_dms = (
            int(dms[0]),
            int(dms[1]),
            float(dms[2])
            )
        
        self.coord_dd = self._dms2dd(self.coord_dms)
    
    
    def _parse_dd(self, dd):
        """
        Private Method: _parse_dd
        
        Parameters:
        dd - {float} The decimal degree representation of the coordinate.
        """
        
        self.coord_dd = float(dd)
        
        self.coord_dms = self._dd2dms(self.coord_dd)
    
    
    def _dd2dms(self, coord):
        """
        Private Method: _dd2dms
        
        Parameters:
        coord - {float} The decimal degree representation of the coordinate.
        
        Returns:
        {3-tuple} A 3-tuple representing the degrees, minutes, and seconds of a
                  coordinate.
        """
        
        import math
        
        if not isinstance(coord, float):
            return
        
        d = math.floor(coord)
        ms = coord - d
        m = 60 * ms
        s = 60 * (m - math.floor(m))
        
        return (int(d), int(m), round(float(s), 6))
    
    
    def _dms2dd(self, coord):
        """
        Private Method: _dms2dd
        
        Parameters:
        coord - {3-tuple} A 3-tuple representing the degrees, minutes, and
                          seconds of a coordinate.
        
        Returns:
        {float} The decimal degree representation of the coordinate.
        """
        
        if len(coord) != 3 or not isinstance(coord, tuple):
            return 0.0
        
        if not isinstance(coord[0], int) or \
           not isinstance(coord[1], int) or \
           not isinstance(coord[2], float):
            return 0.0
        
        dd = coord[0] + (coord[1]/60.0) + (coord[2]/(60.0*60.0))
        
        return round(float(dd), 6)
    
    
    def getDms(self):
        """
        Method: getDms
        
        Returns:
        {string} The degrees-minutes-seconds representation of the coordinate.
        """
        
        if self.coord_dms and self.direction:
            return "%sd %sm %ss %s" % (
                self.coord_dms[0],
                self.coord_dms[1],
                self.coord_dms[2],
                self.direction
                )
        else:
            return None
    
    
    def getDdString(self):
        """
        Method: getDdString
        
        Returns:
        {string} The decimal degree representation of the coordinate with
                 direction. Does not use the negative sign but instead either
                 'W' or 'S'.
        """
        
        if self.coord_dd or (self.coord_dd != None and int(self.coord_dd) == 0) and self.direction:
            return "%s %s" % (
                self.coord_dd,
                self.direction
                )
        else:
            return None
    
    
    def getDdNum(self):
        """
        Method: getDdNum
        
        Returns:
        {string} The decimal degree representation of the coordinate.
        """
        
        if self.direction in ['W', 'S']:
            return "-%s" % self.coord_dd
        else:
            if self.coord_dd or (self.coord_dd != None and int(self.coord_dd) == 0):
                return "%s" % self.coord_dd
            else:
                return None
    
    
    def getDd(self):
        """
        Method: getDd
        
        Returns:
        {string} The decimal degree representation of the coordinate.
        """
        
        return self.getDdNum()
    
    
    def getCoord(self):
        """
        Method: getCoord
        
        Returns:
        {string} The coordinate as entered in by the user.
        """
        
        return "%s" % self.coord
    
    
    def isValid(self):
        """
        Method: isValid
        
        Returns:
        {boolean} True if the coordinate parsing succeeded, False otherwise.
        """
        
        try:
            return (self.coord_dd or int(self.coord_dd) == 0) and self.coord_dms and self.direction
        except:
            return False
    
    
    def debug(self):
        """
        Method: debug
        
        Description:
        Prints debug information.
        """
        
        print "Coord:    %s" % self.getCoord()
        print "DD:       %s" % self.getDd()
        print "DDNum:    %s" % self.getDdNum()
        print "DDString: %s" % self.getDdString()
        print "DMS:      %s" % self.getDms()


class Point:
    """
    Class: Point
    
    Public Methods:
    __init__ - Constructor.
    __str__ - String formatting function.
    geoDistanceTo - Calculates the geographic distance between two points.
    geoBearingTo - Calculates the geographic bearing (from North) between two
                   points.
    geoWaypoint - Returns a <Point> who's coordinates are calculated by the
                  range abd bearing parameters.
    
    Requires:
    <Coordinate> - Coordinate parsing class used in the constructor of this
                   class.
    
    Reference:
    Williams, Ed, 2000, "Aviation Formulary V1.43" web page
    http://williams.best.vwh.net/avform.htm
    """
    
    x = None
    y = None
    
    
    def __init__(self, x, y):
        """
        Method: __init__ (Constructor)
        """
        
        self.x = float(Coordinate(x, "Lon").getDd())
        self.y = float(Coordinate(y, "Lat").getDd())
    
    
    def __str__(self):
        """
        Method: __str__
        
        Description:
        Overloaded print function
        
        Returns:
        {string} The string representation of the point.
        """
        
        return "(%s, %s)" % (self.x, self.y)
    
    
    def geoDistanceTo(self, point, units='km'):
        """
        Method: geoDistanceTo
        
        Parameters:
        point - {<Point>}
        
        Returns:
        {float} Great Circle distance to Point. Coordinates must be in decimal
        degrees.
        """
        
        global EARTH_RADIUS_KM, EARTH_RADIUS_MI, EARTH_RADIUS_NMI, DEG2RAD
        
        x = [0, 0]
        y = [0, 0]
        radius = 0
        
        # Calculates the radius of the earth used
        if units and units.lower() == 'km':
            radius = EARTH_RADIUS_KM
        elif units and units.lower() == 'm':
            radius = EARTH_RADIUS_M
        elif units and units.lower() == 'mi':
            radius = EARTH_RADIUS_MI
        elif units and units.lower() == 'ft':
            radius = EARTH_RADIUS_FT
        elif units and units.lower() == 'nmi':
            radius = EARTH_RADIUS_NMI
        else:
            radius = EARTH_RADIUS_KM
        
        x[0] = self.x * DEG2RAD
        x[1] = point.x * DEG2RAD
        y[0] = self.y * DEG2RAD
        y[1] = point.y * DEG2RAD
        
        a = math.pow( math.sin(( y[1]-y[0] ) / 2.0 ), 2)
        b = math.pow( math.sin(( x[1]-x[0] ) / 2.0 ), 2)
        c = math.pow(( a + math.cos( y[1] ) * math.cos( y[0] ) * b ), 0.5)
        
        return 2 * math.asin( c ) * radius
    
    
    def geoBearingTo(self, point):
        """
        Method: geoBearingTo
        
        Parameters:
        point - {<Point>}
        
        Returns:
        {float} - The bearing clockwise from North in degrees.
        """
        
        global EARTH_RADIUS_KM, EARTH_RADIUS_MI, EARTH_RADIUS_NMI
        global DEG2RAD, RAD2DEG
        
        x = [0, 0]
        y = [0, 0]
        bearing = None
        adjust = None
        
        x[0] = self.x * DEG2RAD
        x[1] = point.x * DEG2RAD
        y[0] = self.y * DEG2RAD
        y[1] = point.y * DEG2RAD
        
        a = math.cos(y[1]) * math.sin(x[1] - x[0])
        b = math.cos(y[0]) * math.sin(y[1]) - math.sin(y[0]) * math.cos(y[1]) * math.cos(x[1] - x[0])
        
        if a == 0 and b == 0:
            return 0.0
        
        if b == 0:
            if a < 0:
                return 270.0
            else:
                return 90.0
        
        if b < 0:
            adjust = math.pi
        else:
            if a < 0:
                adjust = 2 * math.pi
            else:
                adjust = 0
        
        return (math.atan(a/b) + adjust) * RAD2DEG
    
    
    def geoWaypoint(self, distance, bearing, units='km'):
        """
        Method: geoBearingTo
        
        Parameters:
        distance - {float}
        bearing  - {float}
        units    - {string}
        
        Returns:
        {<Point>} - The generated point given by distance and bearing.
        """
        
        global EARTH_RADIUS_KM, EARTH_RADIUS_MI, EARTH_RADIUS_NMI
        global DEG2RAD, RAD2DEG
        
        wp = Point(0, 0)
        radius = 0
        
        # Calculates the radius of the earth used
        if units and units.lower() == 'km':
            radius = EARTH_RADIUS_KM
        elif units and units.lower() == 'm':
            radius = EARTH_RADIUS_M
        elif units and units.lower() == 'mi':
            radius = EARTH_RADIUS_MI
        elif units and units.lower() == 'ft':
            radius = EARTH_RADIUS_FT
        elif units and units.lower() == 'nmi':
            radius = EARTH_RADIUS_NMI
        else:
            radius = EARTH_RADIUS_KM
        
        x = self.x * DEG2RAD
        y = self.y * DEG2RAD
        radBearing = bearing * DEG2RAD
        
        # Convert arc distance to radians
        c = distance / radius
        
        wp.y = math.asin( math.sin(y) * math.cos(c) + math.cos(y) * math.sin(c) * math.cos(radBearing)) * RAD2DEG
        
        a = math.sin(c) * math.sin(radBearing)
        b = math.cos(y) * math.cos(c) - math.sin(y) * math.sin(c) * math.cos(radBearing)
        
        if b == 0:
            wp.x = self.x
        else:
            wp.x = self.x + math.atan(a/b) * RAD2DEG
        
        return wp



