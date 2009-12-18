import coordinate
import unittest

class TestDecimalDegree(unittest.TestCase):
    """
    Class: TestDecimalDegree
    
    Description:
    The unit test cases for testing the Coordinate class' ability to parse and
    represent coordinates using the decimal-degrees (DD) notation "123.1234".
    """
    
    def setUp(self):
        self.coord1 = coordinate.Coordinate("-123.1234")
        self.coord2 = coordinate.Coordinate("-123.1234", "Lon")
        self.coord3 = coordinate.Coordinate("E 123.1234", "Lon")
        self.coord4 = coordinate.Coordinate("S 123.1234", "Lon")
        self.coord5 = coordinate.Coordinate("W 123.1234", "Latitude")
        self.coord6 = coordinate.Coordinate("123.1234N", "Long")
        self.coord7 = coordinate.Coordinate("N123.1234N", "Long")
        self.coord8 = coordinate.Coordinate("           -         123.1234              ", "Long")
        self.coord9 = coordinate.Coordinate("-146.542123", "LoNgItUdE")
        self.coord10 = coordinate.Coordinate("W146.54212354", "LoNgItUdE")
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord1, coordinate.Coordinate))
        self.assert_(isinstance(self.coord2, coordinate.Coordinate))
        self.assert_(isinstance(self.coord3, coordinate.Coordinate))
        self.assert_(isinstance(self.coord4, coordinate.Coordinate))
        self.assert_(isinstance(self.coord5, coordinate.Coordinate))
        self.assert_(isinstance(self.coord6, coordinate.Coordinate))
        self.assert_(isinstance(self.coord7, coordinate.Coordinate))
        self.assert_(isinstance(self.coord8, coordinate.Coordinate))
        self.assert_(isinstance(self.coord9, coordinate.Coordinate))
        self.assert_(isinstance(self.coord10, coordinate.Coordinate))
    
    def test_Coord(self):
        self.assertEquals(self.coord1.getCoord(), "-123.1234")
        self.assertEquals(self.coord2.getCoord(), "-123.1234")
        self.assertEquals(self.coord3.getCoord(), "E 123.1234")
        self.assertEquals(self.coord4.getCoord(), "S 123.1234")
        self.assertEquals(self.coord5.getCoord(), "W 123.1234")
        self.assertEquals(self.coord6.getCoord(), "123.1234N")
        self.assertEquals(self.coord7.getCoord(), "N123.1234N")
        self.assertEquals(self.coord8.getCoord(), "           -         123.1234              ")
        self.assertEquals(self.coord9.getCoord(), "-146.542123")
        self.assertEquals(self.coord10.getCoord(), "W146.54212354")
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord1.getDdNum(), self.coord1.getDd())
        self.assertEquals(self.coord2.getDdNum(), self.coord2.getDd())
        self.assertEquals(self.coord3.getDdNum(), self.coord3.getDd())
        self.assertEquals(self.coord4.getDdNum(), self.coord4.getDd())
        self.assertEquals(self.coord5.getDdNum(), self.coord5.getDd())
        self.assertEquals(self.coord6.getDdNum(), self.coord6.getDd())
        self.assertEquals(self.coord7.getDdNum(), self.coord7.getDd())
        self.assertEquals(self.coord8.getDdNum(), self.coord8.getDd())
        self.assertEquals(self.coord9.getDdNum(), self.coord9.getDd())
        self.assertEquals(self.coord10.getDdNum(), self.coord10.getDd())
    
    def test_Dd(self):
        self.assertEquals(self.coord1.getDd(), "-123.1234")
        self.assertEquals(self.coord2.getDd(), "-123.1234")
        self.assertEquals(self.coord3.getDd(), "123.1234")
        self.assertEquals(self.coord4.getDd(), "-123.1234")
        self.assertEquals(self.coord5.getDd(), "-123.1234")
        self.assertEquals(self.coord6.getDd(), "123.1234")
        self.assertEquals(self.coord7.getDd(), None)
        self.assertEquals(self.coord8.getDd(), "-123.1234")
        self.assertEquals(self.coord9.getDd(), "-146.542123")
        self.assertEquals(self.coord10.getDd(), "-146.54212354")
    
    def test_DdString(self):
        self.assertEquals(self.coord1.getDdString(), "123.1234 S")
        self.assertEquals(self.coord2.getDdString(), "123.1234 W")
        self.assertEquals(self.coord3.getDdString(), "123.1234 E")
        self.assertEquals(self.coord4.getDdString(), "123.1234 S")
        self.assertEquals(self.coord5.getDdString(), "123.1234 W")
        self.assertEquals(self.coord6.getDdString(), "123.1234 N")
        self.assertEquals(self.coord7.getDdString(), None)
        self.assertEquals(self.coord8.getDdString(), "123.1234 W")
        self.assertEquals(self.coord9.getDdString(), "146.542123 W")
        self.assertEquals(self.coord10.getDdString(), "146.54212354 W")
    
    def test_Dms(self):
        self.assertEquals(self.coord1.getDms(), "123d 7m 24.24s S")
        self.assertEquals(self.coord2.getDms(), "123d 7m 24.24s W")
        self.assertEquals(self.coord3.getDms(), "123d 7m 24.24s E")
        self.assertEquals(self.coord4.getDms(), "123d 7m 24.24s S")
        self.assertEquals(self.coord5.getDms(), "123d 7m 24.24s W")
        self.assertEquals(self.coord6.getDms(), "123d 7m 24.24s N")
        self.assertEquals(self.coord7.getDms(), None)
        self.assertEquals(self.coord8.getDms(), "123d 7m 24.24s W")
        self.assertEquals(self.coord9.getDms(), "146d 32m 31.6428s W")
        self.assertEquals(self.coord10.getDms(), "146d 32m 31.644744s W")



class TestDegreesMinutesSeconds(unittest.TestCase):
    """
    Class: TestDegreesMinutesSeconds
    
    Description:
    The unit test cases for testing the Coordinate class' ability to parse and
    represent coordinates using the degrees-minutes-seconds (DMS) notation
    "11d 22m 33.333333s N".
    """
    
    def setUp(self):
        self.coord1 = coordinate.Coordinate("11d 22m 33.333s", "Longitude")
        self.coord2 = coordinate.Coordinate("-22d33m44.444444s")
        self.coord3 = coordinate.Coordinate("E22d33m44.444444s")
        self.coord4 = coordinate.Coordinate("     1   d    9   m    0s   W     ", "lat")
        self.coord5 = coordinate.Coordinate("E2222d3333m4444.444444s", "Latitude")
    
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord1, coordinate.Coordinate))
        self.assert_(isinstance(self.coord2, coordinate.Coordinate))
        self.assert_(isinstance(self.coord3, coordinate.Coordinate))
        self.assert_(isinstance(self.coord4, coordinate.Coordinate))
        self.assert_(isinstance(self.coord5, coordinate.Coordinate))
    
    
    def test_Coord(self):
        self.assertEquals(self.coord1.getCoord(), "11d 22m 33.333s")
        self.assertEquals(self.coord2.getCoord(), "-22d33m44.444444s")
        self.assertEquals(self.coord3.getCoord(), "E22d33m44.444444s")
        self.assertEquals(self.coord4.getCoord(), "     1   d    9   m    0s   W     ")
        self.assertEquals(self.coord5.getCoord(), "E2222d3333m4444.444444s")
    
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord1.getDdNum(), self.coord1.getDd())
        self.assertEquals(self.coord2.getDdNum(), self.coord2.getDd())
        self.assertEquals(self.coord3.getDdNum(), self.coord3.getDd())
        self.assertEquals(self.coord4.getDdNum(), self.coord4.getDd())
        self.assertEquals(self.coord5.getDdNum(), self.coord5.getDd())
    
    
    def test_Dd(self):
        self.assertEquals(self.coord1.getDd(), "11.375926")
        self.assertEquals(self.coord2.getDd(), "-22.562346")
        self.assertEquals(self.coord3.getDd(), "22.562346")
        self.assertEquals(self.coord4.getDd(), "-1.15")
        self.assertEquals(self.coord5.getDd(), None)
    
    
    def test_DdString(self):
        self.assertEquals(self.coord1.getDdString(), "11.375926 E")
        self.assertEquals(self.coord2.getDdString(), "22.562346 S")
        self.assertEquals(self.coord3.getDdString(), "22.562346 E")
        self.assertEquals(self.coord4.getDdString(), "1.15 W")
        self.assertEquals(self.coord5.getDdString(), None)
    
    
    def test_Dms(self):
        self.assertEquals(self.coord1.getDms(), "11d 22m 33.333s E")
        self.assertEquals(self.coord2.getDms(), "22d 33m 44.444444s S")
        self.assertEquals(self.coord3.getDms(), "22d 33m 44.444444s E")
        self.assertEquals(self.coord4.getDms(), "1d 9m 0.0s W")
        self.assertEquals(self.coord5.getDms(), None)



class TestDegreesMinutesSecondsColon(unittest.TestCase):
    """
    Class: TestDegreesMinutesSecondsColon
    
    Description:
    The unit test cases for testing the Coordinate class' ability to parse and
    represent coordinates using the degrees-minutes-seconds (DMS) notation
    "11:22:33.333333 N".
    """
    
    def setUp(self):
        self.coord1 = coordinate.Coordinate("11: 22: 33.333", "Longitude")
        self.coord2 = coordinate.Coordinate("-22:33:44.444444")
        self.coord3 = coordinate.Coordinate("E22:33:44.444444")
        self.coord4 = coordinate.Coordinate("     1   :    9   :    0   W     ", "lat")
        self.coord5 = coordinate.Coordinate("E2222:3333:4444.444444", "Latitude")
    
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord1, coordinate.Coordinate))
        self.assert_(isinstance(self.coord2, coordinate.Coordinate))
        self.assert_(isinstance(self.coord3, coordinate.Coordinate))
        self.assert_(isinstance(self.coord4, coordinate.Coordinate))
        self.assert_(isinstance(self.coord5, coordinate.Coordinate))
    
    
    def test_Coord(self):
        self.assertEquals(self.coord1.getCoord(), "11: 22: 33.333")
        self.assertEquals(self.coord2.getCoord(), "-22:33:44.444444")
        self.assertEquals(self.coord3.getCoord(), "E22:33:44.444444")
        self.assertEquals(self.coord4.getCoord(), "     1   :    9   :    0   W     ")
        self.assertEquals(self.coord5.getCoord(), "E2222:3333:4444.444444")
    
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord1.getDdNum(), self.coord1.getDd())
        self.assertEquals(self.coord2.getDdNum(), self.coord2.getDd())
        self.assertEquals(self.coord3.getDdNum(), self.coord3.getDd())
        self.assertEquals(self.coord4.getDdNum(), self.coord4.getDd())
        self.assertEquals(self.coord5.getDdNum(), self.coord5.getDd())
    
    
    def test_Dd(self):
        self.assertEquals(self.coord1.getDd(), "11.375926")
        self.assertEquals(self.coord2.getDd(), "-22.562346")
        self.assertEquals(self.coord3.getDd(), "22.562346")
        self.assertEquals(self.coord4.getDd(), "-1.15")
        self.assertEquals(self.coord5.getDd(), None)
    
    
    def test_DdString(self):
        self.assertEquals(self.coord1.getDdString(), "11.375926 E")
        self.assertEquals(self.coord2.getDdString(), "22.562346 S")
        self.assertEquals(self.coord3.getDdString(), "22.562346 E")
        self.assertEquals(self.coord4.getDdString(), "1.15 W")
        self.assertEquals(self.coord5.getDdString(), None)
    
    
    def test_Dms(self):
        self.assertEquals(self.coord1.getDms(), "11d 22m 33.333s E")
        self.assertEquals(self.coord2.getDms(), "22d 33m 44.444444s S")
        self.assertEquals(self.coord3.getDms(), "22d 33m 44.444444s E")
        self.assertEquals(self.coord4.getDms(), "1d 9m 0.0s W")
        self.assertEquals(self.coord5.getDms(), None)



class TestPoint(unittest.TestCase):
    """
    Class: TestPoint
    
    Description:
    The unit test cases for testing the Point class' ability to parse
    coordinates (using Coordinate class) and then do geographic calculations
    with those points (distance, bearing, and generating a new point).
    """
    
    def setUp(self):
        self.p1 = coordinate.Point(0, 0)
        self.p2 = coordinate.Point(0, 1)
        self.p3 = coordinate.Point(0, -1)
        self.p4 = coordinate.Point(1, 0)
        self.p5 = coordinate.Point(-1, 0)
    
    
    def test_RangeKm(self):
        self.assertEquals(self.p1.geoDistanceTo(self.p2), 111.19508372455267)
        self.assertEquals(self.p2.geoDistanceTo(self.p1), 111.19508372455267)
        self.assertEquals(self.p1.geoDistanceTo(self.p2, 'km'), self.p2.geoDistanceTo(self.p1, 'KM'))
        self.assertEquals(self.p1.geoDistanceTo(self.p3), self.p2.geoDistanceTo(self.p1))
        self.assertEquals(self.p1.geoDistanceTo(self.p4), self.p1.geoDistanceTo(self.p3))
        self.assertEquals(self.p1.geoDistanceTo(self.p5), self.p4.geoDistanceTo(self.p1))
        self.assertEquals(self.p2.geoDistanceTo(self.p3), self.p4.geoDistanceTo(self.p5))
    
    
    def test_RangeMi(self):
        self.assertEquals(self.p1.geoDistanceTo(self.p2, 'mi'), 69.09341374976772)
        self.assertEquals(self.p2.geoDistanceTo(self.p1, 'mi'), 69.09341374976772)
        self.assertEquals(self.p1.geoDistanceTo(self.p2, 'mi'), self.p2.geoDistanceTo(self.p1, 'MI'))
        self.assertEquals(self.p1.geoDistanceTo(self.p3, 'mi'), self.p2.geoDistanceTo(self.p1, 'mi'))
        self.assertEquals(self.p1.geoDistanceTo(self.p4, 'mi'), self.p1.geoDistanceTo(self.p3, 'mi'))
        self.assertEquals(self.p1.geoDistanceTo(self.p5, 'mi'), self.p4.geoDistanceTo(self.p1, 'mi'))
        self.assertEquals(self.p2.geoDistanceTo(self.p3, 'mi'), self.p4.geoDistanceTo(self.p5, 'mi'))
    
    
    def test_RangeNmi(self):
        self.assertEquals(self.p1.geoDistanceTo(self.p2, 'nmi'), 60.040530545983877)
        self.assertEquals(self.p2.geoDistanceTo(self.p1, 'nmi'), 60.040530545983877)
        self.assertEquals(self.p1.geoDistanceTo(self.p2, 'nmi'), self.p2.geoDistanceTo(self.p1, 'nMI'))
        self.assertEquals(self.p1.geoDistanceTo(self.p3, 'nmi'), self.p2.geoDistanceTo(self.p1, 'nmi'))
        self.assertEquals(self.p1.geoDistanceTo(self.p4, 'nmi'), self.p1.geoDistanceTo(self.p3, 'nmi'))
        self.assertEquals(self.p1.geoDistanceTo(self.p5, 'nmi'), self.p4.geoDistanceTo(self.p1, 'nmi'))
        self.assertEquals(self.p2.geoDistanceTo(self.p3, 'nmi'), self.p4.geoDistanceTo(self.p5, 'nmi'))
    
    
    def test_Bearing(self):
        self.assertEquals(self.p2.geoBearingTo(self.p1), 179.9999999999927)
        self.assertEquals(self.p1.geoBearingTo(self.p2), 0.0)
        self.assertEquals(self.p2.geoBearingTo(self.p3), 179.9999999999927)
        self.assertEquals(self.p3.geoBearingTo(self.p2), 0.0)
        self.assertEquals(self.p1.geoBearingTo(self.p4), 90.0)
        self.assertEquals(self.p4.geoBearingTo(self.p1), 270.0)
        self.assertEquals(self.p1.geoBearingTo(self.p5), 270.0)
        self.assertEquals(self.p5.geoBearingTo(self.p1), 90.0)
    
    
    def test_Waypoint(self):
        p1 = self.p1
        self.assertEquals(p1.__str__(), "(0.0, 0.0)")
        p2 = p1.geoWaypoint(100, 0)
        self.assertEquals(p2.__str__(), "(0.0, 0.899320335493)")
        p3 = p1.geoWaypoint(100, 45)
        self.assertEquals(p3.__str__(), "(0.635941619825, 0.635902451374)")
        p4 = p1.geoWaypoint(100, 90)
        self.assertEquals(p4.__str__(), "(0.899320335493, -4.58941371001e-12)")
        p5 = p1.geoWaypoint(100, 135)
        self.assertEquals(p5.__str__(), "(0.635941619819, -0.635902451381)")
        p6 = p1.geoWaypoint(100, 180)
        self.assertEquals(p6.__str__(), "(-9.17995821886e-12, -0.899320335493)")
        p7 = p1.geoWaypoint(100, 225)
        self.assertEquals(p7.__str__(), "(-0.635941619832, -0.635902451368)")
        p8 = p1.geoWaypoint(100, 270)
        self.assertEquals(p8.__str__(), "(-0.899320335493, 1.376824113e-11)")
        p9 = p1.geoWaypoint(100, 315)
        self.assertEquals(p9.__str__(), "(-0.635941619812, 0.635902451387)")
        p10 = p1.geoWaypoint(100, 360)
        self.assertEquals(p10.__str__(), "(1.83599164377e-11, 0.899320335493)")



def runtests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDecimalDegree)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDegreesMinutesSeconds))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDegreesMinutesSecondsColon))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPoint))
    unittest.TextTestRunner(verbosity=2).run(suite)

