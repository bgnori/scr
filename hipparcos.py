
import ephem
import I239
import sys


def degree2rad(deg):
    return deg/180. * ephem.pi


def makestar(epoch, ra, dec, name):
    """
        FixedBody can't have args.... it's a bug in ephem
    """
    s = ephem.FixedBody()
    s._epoch=epoch
    s._ra=ra
    print s._ra
    s._dec=dec
    print s._dec
    s.name=name
    return s 



J1991_25 = 2448349.0625 #TT
"""
    expressed in degrees for epoch J1991.25 (JD2448349.0625 (TT)) in the
"""

J2000 = 2451545.0  #TT
"""
    http://en.wikipedia.org/wiki/Equinox_%28celestial_coordinates%29#J2000.0
"""

def TT2DJD(tt):
    """
        conversion from TT to Dublin Julian Date
        see http://en.wikipedia.org/wiki/Julian_day
        TT is 
    """
    return tt - 2415020.0

EPHEMJ1991_25 = ephem.Date(TT2DJD(J1991_25))


POLARIS_DATA = """H|       11767| |02 31 47.08|+89 15 50.9| 1.97|1|H|037.94614689|+89.26413805| |   7.56|   44.22|  -11.74|  0.39|  0.45|  0.48|  0.47|  0.55|-0.16| 0.05| 0.27|-0.01| 0.08| 0.05| 0.04|-0.12|-0.09|-0.36|  1| 1.22| 11767| 2.756|0.003| 2.067|0.003| | 0.636|0.003|T|0.70|0.00|L| | 2.1077|0.0021|0.014|102| | 2.09| 2.13|   3.97|P|1|A|02319+8915|I| 1| 1| | | |  |   |       |     |     |    |S| |P|  8890|B+88    8 |          |          |0.68|F7:Ib-IIv SB|G """

with open("hip_main.description") as f:
    parser = I239.ParserBuilder(f.read())


catalogue = {}
#with open("../hipparcos/I239/hip_main.dat") as f:
#    for n in xrange(20000):
#        line = f.readline()
if True:
    if True:
        line = POLARIS_DATA
        entry = parser.parse(line)


        try:
            catalogue[entry["HIP"]] = makestar(
                    EPHEMJ1991_25, 
                    ephem.hours(degree2rad(entry["RAdeg"])),
                    ephem.degrees(degree2rad(entry["DEdeg"])),
                    "HIP=%i"%(entry["HIP"]))
        except:
            print >> sys.stderr, entry


tokyo = ephem.Observer()
tokyo.lat = "60.0"
tokyo.lon = "-139.0"
tokyo.elevation = 40
tokyo.date = ephem.J2000

# 11767 is Polaris.
Polaris = catalogue[11767]
Polaris.compute(tokyo)
print "Polaris is HIP 11767... got ", Polaris.name 
print "ra should be 2h31m49.09s, dec should be +89 15.50'50.8\""
print entry["RAdeg"], entry["DEdeg"]
print degree2rad(entry["RAdeg"]), degree2rad(entry["DEdeg"])
print '----'
print "ra=%s, dec=%s"%(Polaris.ra, Polaris.dec)
print "a_ra=%s, a_dec=%s"%(Polaris.a_ra, Polaris.a_dec)
print "a_ra=%f, a_dec=%f"%(Polaris.a_ra, Polaris.a_dec)
print "az=%s, alt=%s"%(Polaris.az, Polaris.alt)


