"""
Coordinate library

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

class Coordinate:
    coord = None     # string
    
    coord_dd = None  # real number
    coord_dms = None # 3-tuple
    is_valid = False # boolean
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
    
    # @param  coord  string
    # @param  axis   string
    def __init__(self, coord, axis=''):
        self.coord = str(coord)
        self._parse(axis)
    
    # @param  axis  string
    def _parse(self, axis=''):
        position = 1
        for r in self.regs:
            m = r.match(self.coord)
            if m:
                self.groups = m.groups()
                break
            else:
                position += 1
                continue
        
        if not self.groups:
            return
        
        # Parse direction and coordinate
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
    
    # @param  direction  string
    # @param  axis       string
    def _parse_direction(self, direction, axis):
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
    
    # dms is a 3-tuple
    def _parse_dms(self, dms):
        if len(dms) != 3 or not isinstance(dms, tuple):
            return
        
        self.coord_dms = (
            int(dms[0]),
            int(dms[1]),
            float(dms[2])
            )
        
        self.coord_dd = self._dms2dd(self.coord_dms)
    
    # @param  dd float
    def _parse_dd(self, dd):
        self.coord_dd = float(dd)
        
        self.coord_dms = self._dd2dms(self.coord_dd)
    
    # @param  coord float
    # @return       3-tuple
    def _dd2dms(self, coord):
        import math
        
        if not isinstance(coord, float):
            return
        
        d = math.floor(coord)
        ms = coord - d
        m = 60 * ms
        s = 60 * (m - math.floor(m))
        
        return (int(d), int(m), float(s))
    
    # @param  coord 3-tuple
    # @return       float
    def _dms2dd(self, coord):
        if len(coord) != 3 or not isinstance(coord, tuple):
            return 0.0
        
        if not isinstance(coord[0], int) or \
           not isinstance(coord[1], int) or \
           not isinstance(coord[2], float):
            return 0.0
        
        dd = coord[0] + (coord[1]/60.0) + (coord[2]/(60.0*60.0))
        
        return dd
    
    # @return string
    def getDms(self):
        return "%sd %sm %ss %s" % (
            self.coord_dms[0],
            self.coord_dms[1],
            self.coord_dms[2],
            self.direction
            )
    
    # @return string
    def getDdString(self):
        return "%s %s" % (
            self.coord_dd,
            self.direction
            )
    
    # @return string
    def getDdNum(self):
        if self.direction in ['W', 'S']:
            return "-%s" % self.coord_dd
        else:
            return "%s" % self.coord_dd
    
    # @return string
    def getDd(self):
        return self.getDdNum()
    
    # @return string
    def getCoord(self):
        return "%s" % self.coord
