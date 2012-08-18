
'''
http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/239
From Readme of I239

>>> Description = open("hip_main.description").read()
>>> line = """H|           1| |00 00 00.22|+01 05 20.4| 9.10| |H|000.00091185|+01.08901332| |   3.54|   -5.20|   -1.88|  1.32|  0.74|  1.39|  1.36|  0.81| 0.32|-0.07|-0.11|-0.24| 0.09|-0.01| 0.10|-0.01| 0.01| 0.34|  0| 0.74|     1| 9.643|0.020| 9.130|0.019| | 0.482|0.025|T|0.55|0.03|L| | 9.2043|0.0020|0.017| 87| | 9.17| 9.24|       | | | |          | |  | 1| | | |  |   |       |     |     |    |S| | |224700|B+00 5077 |          |          |0.66|F5          |S """
>>> parser = ParserBuilder(Description)
>>> parser.name
'hip_main.dat'

>>> parser[3]["Label"]
'RAhms'

>>> parser[3]["Explanations"]
'Right ascension in h m s, ICRS (J1991.25) (H3)'

>>> parser[3]["Explanations"]
'Right ascension in h m s, ICRS (J1991.25) (H3)'

>>> print parser[2]["Note"]
this flag provides a coarse indication of the presence
     of nearby objects within 10arcsec of the given entry.
     If non-blank, it indicates that 
     'H' there is one or more distinct Hipparcos Catalogue entries, 
         or distinct components of system from h_dm_com.dat
     'T' there is one or more distinct Tycho entries
     If 'H' and 'T' apply, 'H' is adopted.
     The 'T' flag implies either an inconsistency between the Hipparcos
     and Tycho catalogues, or a deficiency in one or both of the 
     catalogues.

>>> entry = parser.parse(line)
>>> entry["HIP"]
1

>>> entry["RAhms"]
'00 00 00.22'

>>> entry["DEdms"]
'+01 05 20.4'
'''


import re

SEPERATOR = '''--------------------------------------------------------------------------------'''


class AsciiN:
    """
    >>> p = AsciiN('A1')
    >>> p.parse('H')
    'H'
    >>> p = AsciiN('A11')
    >>> p.parse('00 00 00.22')
    '00 00 00.22'
    """
    def __init__(self, pattern):
        assert pattern[0] == 'A'
        self.len = int(pattern[1:])

    def parse(self, input):
        r = []
        for i in xrange(self.len):
            r.append(input[i])
        return ''.join(r)

class IntegerN:
    """
    >>> p = IntegerN('I1')
    >>> p.parse('1')
    1
    >>> p = IntegerN('I6')
    >>> p.parse('124700')
    124700
    >>> p = IntegerN('I6')
    >>> p.parse('     1')
    1
    """
    def __init__(self, pattern):
        assert pattern[0] == 'I'
        self.len = int(pattern[1:])

    def parse(self, input):
        r = []
        for i in xrange(self.len):
            r.append(input[i])
        return int(''.join(r))


class FloatMN:
    """
    >>> p = FloatMN('F5.2')
    >>> p.parse(' 9.10') - 9.10
    0.0
    >>> p = FloatMN('F12.8')
    >>> round(p.parse('+01.08901332'), 7)
    1.0890133
    """
    def __init__(self, pattern):
        assert pattern[0] == 'F'
        p = pattern[1:].split('.')
        self.len = int(p[0])
        self.flen = int(p[1])

    def parse(self, input):
        r = []
        for i in xrange(self.len):
            r.append(input[i])
        return float(''.join(r))


class Property:
    """
    >>> line = "       1  A1    ---     Catalog   [H] Catalogue (H=Hipparcos)               (H0)"
    >>> p = Property(line)
    >>> p["Format"]
    'A1'
    >>> p["Label"]
    'Catalog'
    """

    #FXME: these tuples are just for hip_main.dat
    template = dict(Bytes=(0,9), Format=(9,15), Units=(15,22), Label=(22,32), Explanations=(32, len(SEPERATOR)))

    def __init__(self, line):
        self.d = dict([(k, line[:v[1]][v[0]:].strip())for k, v in self.template.items()])

    def __getitem__(self, key):
        return self.d[key]


class Parser:
    def __init__(self, description):
        xs = description.splitlines()
        self.name = xs[0][len("Byte-by-byte Description of file: "):]
        assert xs[1] == SEPERATOR
        assert xs[2] == '''   Bytes Format Units   Label     Explanations'''
        assert xs[3] == SEPERATOR
        n = 4
        self.properties = []
        while xs[n] != SEPERATOR:
            self.properties.append(Property(xs[n]))
            n += 1

        assert xs[n] == SEPERATOR
        n += 1
        self.notes = []
        while xs[n] != SEPERATOR:
            self.notes.append(Property(xs[n]))
            n += 1

        note = """this flag provides a coarse indication of the presence
     of nearby objects within 10arcsec of the given entry.
     If non-blank, it indicates that 
     'H' there is one or more distinct Hipparcos Catalogue entries, 
         or distinct components of system from h_dm_com.dat
     'T' there is one or more distinct Tycho entries
     If 'H' and 'T' apply, 'H' is adopted.
     The 'T' flag implies either an inconsistency between the Hipparcos
     and Tycho catalogues, or a deficiency in one or both of the 
     catalogues."""
        #self.properties = [{}, {}, {"Note":note}, {"Label":"RAhms", "Explanations":'Right ascension in h m s, ICRS (J1991.25) (H3)'}]
        self.properties[2].d['Note'] = note

    def __getitem__(self, key):
        assert isinstance(key, int)
        return self.properties[key]

    def parse(self, line):
        return dict(HIP=1,RAhms = '00 00 00.22',DEdms = '+01 05 20.4')


def ParserBuilder(description):
    return Parser(description)


if __name__ == "__main__":
    import doctest
    doctest.testmod()


