
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

>>> tyc_Description = open("tyc_main.description").read()
>>> tyc_line = """T|4628   237 1| |02 31 47.08|+89 15 50.9| 2.00| | |037.94616079|+89.26413807|X|   8.5 |   45.5 |  -14.3 |  1.2 |  1.4 |  1.4 |  1.4 |  1.7 |-0.22|+0.24|+0.05|-0.25|+0.23|-0.07|+0.20|-0.48|+0.09|-0.43|142| 0.12| 11767| 2.756|0.003| 2.067|0.003|M| 0.620|0.003| |1|12.5| |130|0.032| 2.04| 2.10|G|W|Y|A|  |   431|  8890|B+88    8 |          |          |L"""

>>> tyc_parser = ParserBuilder(tyc_Description)
>>> tyc_parser.name
'tyc_main.dat'

>>> tyc_parser[3]["Label"]
'RAhms'

>>> entry = tyc_parser.parse(tyc_line)
>>> entry["TYC"]
'4628   237 1'


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
        return input[:self.len]

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
        r = input[:self.len].strip()
        assert r
        for c in r:
            assert c in '-+0123456789'
        return int(r)


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
        r = input[:self.len].strip()
        assert r
        for c in r:
            assert c in '-+.0123456789'
        return float(r)


def get_parser(pattern):
    if pattern[0]=='A':
        return AsciiN(pattern)
    elif pattern[0] == 'I':
        return IntegerN(pattern)
    elif pattern[0] == 'F':
        return FloatMN(pattern)
    else:
        assert False


def get_range(s):
    if '-' in s:
        b, e = s.split('-')
        return (int(b) - 1, int(e))
    else:
        b = int(s) -1
        return (b, b+1)


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

    def __setitem__(self, key, value):
        self.d[key] = value


def read_note(notes, actives, line):
    if line[0] == ' ':
        for a in actives:
            notes[a] += ( "\n" + line)
        return actives
    elif line.startswith("Note on "):
        labels, sep, rest = line[len("Note on "):].partition(":")
        xs = [ label.strip() for label in labels.split(',')]
        for x in xs:
            notes[x] = rest
        return xs
    else:
        # Maybe ---- , and it is end of Data
        return None



class Parser:
    def __init__(self, description):
        xs = description.splitlines()
        self.name = xs[0][len("Byte-by-byte Description of file: "):]
        assert xs[1] == SEPERATOR
        assert xs[2].split() == ["Bytes", "Format", "Units", "Label", "Explanations"]

        assert xs[3] == SEPERATOR
        n = 4
        self.properties = []
        while xs[n] != SEPERATOR:
            self.properties.append(Property(xs[n]))
            n += 1

        assert xs[n] == SEPERATOR
        n += 1
        notes = {}
        active = None
        while xs[n] != SEPERATOR:
            active = read_note(notes, active, xs[n])
            n += 1

        for p in self.properties:
            p["Note"] = notes.get(p["Label"], None)

    def __getitem__(self, key):
        assert isinstance(key, int)
        return self.properties[key]

    def parse(self, line):
        d = {}
        for p in self.properties:
            r = get_range(p["Bytes"])
            v = line[r[0]:r[1]].strip()
            if v:
                d[p["Label"]]=get_parser(p["Format"]).parse(v)
            else:
                d[p["Label"]]=None

        return d 


def ParserBuilder(description):
    return Parser(description)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

