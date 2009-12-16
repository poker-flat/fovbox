import coordinate
import unittest

class TestBasicDecimalDegreeNoLatlon(unittest.TestCase):
    def setUp(self):
        self.coord = coordinate.Coordinate("-123.1234")
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord, coordinate.Coordinate))
    
    def test_Coord(self):
        self.assertEquals(self.coord.getCoord(), "-123.1234")
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord.getDdNum(), self.coord.getDd())
    
    def test_Dd(self):
        self.assertEquals(self.coord.getDd(), "-123.1234")
    
    def test_Dms(self):
        self.assertEquals(self.coord.getDms(), "123d 7m 24.24s S")

class TestBasicDecimalDegreeLon(unittest.TestCase):
    def setUp(self):
        self.coord = coordinate.Coordinate("-123.1234", "Lon")
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord, coordinate.Coordinate))
    
    def test_Coord(self):
        self.assertEquals(self.coord.getCoord(), "-123.1234")
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord.getDdNum(), self.coord.getDd())
    
    def test_Dd(self):
        self.assertEquals(self.coord.getDd(), "-123.1234")
    
    def test_Dms(self):
        self.assertEquals(self.coord.getDms(), "123d 7m 24.24s W")

class TestBasicDecimalDegreeELon(unittest.TestCase):
    def setUp(self):
        self.coord = coordinate.Coordinate("E 123.1234", "Lon")
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord, coordinate.Coordinate))
    
    def test_Coord(self):
        self.assertEquals(self.coord.getCoord(), "E 123.1234")
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord.getDdNum(), self.coord.getDd())
    
    def test_Dd(self):
        self.assertEquals(self.coord.getDd(), "123.1234")
    
    def test_Dms(self):
        self.assertEquals(self.coord.getDms(), "123d 7m 24.24s E")

class TestBasicDecimalDegreeSLon(unittest.TestCase):
    def setUp(self):
        self.coord = coordinate.Coordinate("S 123.1234", "Lon")
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord, coordinate.Coordinate))
    
    def test_Coord(self):
        self.assertEquals(self.coord.getCoord(), "S 123.1234")
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord.getDdNum(), self.coord.getDd())
    
    def test_Dd(self):
        self.assertEquals(self.coord.getDd(), "-123.1234")
    
    def test_Dms(self):
        self.assertEquals(self.coord.getDms(), "123d 7m 24.24s S")

class TestBasicDecimalDegreeWLat(unittest.TestCase):
    def setUp(self):
        self.coord = coordinate.Coordinate("W 123.1234", "Latitude")
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord, coordinate.Coordinate))
    
    def test_Coord(self):
        self.assertEquals(self.coord.getCoord(), "W 123.1234")
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord.getDdNum(), self.coord.getDd())
    
    def test_Dd(self):
        self.assertEquals(self.coord.getDd(), "-123.1234")
    
    def test_Dms(self):
        self.assertEquals(self.coord.getDms(), "123d 7m 24.24s W")

class TestBasicDecimalDegreeNLong(unittest.TestCase):
    def setUp(self):
        self.coord = coordinate.Coordinate("123.1234N", "Long")
    
    def test_instanceOfCoord(self):
        self.assert_(isinstance(self.coord, coordinate.Coordinate))
    
    def test_Coord(self):
        self.assertEquals(self.coord.getCoord(), "123.1234N")
    
    def test_DdNumEqualsDd(self):
        self.assertEquals(self.coord.getDdNum(), self.coord.getDd())
    
    def test_Dd(self):
        self.assertEquals(self.coord.getDd(), "123.1234")
    
    def test_Dms(self):
        self.assertEquals(self.coord.getDms(), "123d 7m 24.24s N")

def runtests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasicDecimalDegreeNoLatlon)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBasicDecimalDegreeLon))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBasicDecimalDegreeELon))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBasicDecimalDegreeSLon))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBasicDecimalDegreeWLat))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestBasicDecimalDegreeNLong))
    unittest.TextTestRunner(verbosity=2).run(suite)

