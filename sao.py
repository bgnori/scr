import sys
import re

class ValueSpec:
    def __init__(self, type_info, type_length, description):
        self.type_info = type_info
        self.type_length = type_length
        self.description = description

    def parse(self, s):
        assert False


class CharN(ValueSpec):
    def parse(self, s):
        assert len(s) <= self.type_length
        return s

class IntN(ValueSpec):
    def parse(self, s):
        return int(s)

class Float8(ValueSpec):
    def parse(self, s):
        return float(s)

MAP = dict(float=Float8, int=IntN, char=CharN)

VALUESPEC = re.compile("field\[(?P<name>\w+)\] = (?P<type>[a-zA-Z]+)(?P<length>[0-9]+)(?P<description>.*$)")
def parse_valuespec(line):
    """
        >>> line = '''field[name] = char10  [meta.id;meta.main] (index) // SAO Catalog Designation'''
        >>> c = parse_valuespec(line)
        >>> c #doctest: +ELLIPSIS
        ('name', <__main__.CharN instance at ...>)
        >>> c[1].type_length
        10

        >>> line = '''field[ref_vmag] = int1:2d  [meta.ref;phot.mag;em.opt.V]  // Reference Code for Visual Magnitude'''
        >>> c = parse_valuespec(line)
        >>> c #doctest: +ELLIPSIS
        ('ref_vmag', <__main__.IntN instance at ...>)
        >>> c[1].type_info
        'int'

        >>> line = '''field[num_source_cat] = int4:5d  [meta.id]  // Number in Source Catalog'''
        >>> c = parse_valuespec(line)
        >>> c #doctest: +ELLIPSIS
        ('num_source_cat', <__main__.IntN instance at ...>)

        >>> line = '''field[ra] = float8:.6f_degree [pos.eq.ra;meta.main] (key) // Right Ascension'''
        >>> c = parse_valuespec(line)
        >>> c #doctest: +ELLIPSIS
        ('ra', <__main__.Float8 instance at ...>)
        >>> c[1].type_info
        'float'

    """
    assert line.startswith("field[")
    m = VALUESPEC.search(line)
    d = m.groupdict()
    klass = MAP[d['type']]
    return d['name'], klass(d['type'], int(d['length']), d['description'])


class Parser:
    """
    >>> f = open('sao-text.description')
    >>> p = Parser(f)
    >>> f.close()
    >>> p.items
    ['name', 'ra', 'proper_motion_ra', 'proper_motion_ra_error', 'ra_epoch', 'dec', 'proper_motion_dec', 'proper_motion_dec_error', 'dec_epoch', 'position_error', 'lii', 'bii', 'pg_mag', 'vmag', 'spect_type', 'ref_vmag', 'ref_star_number', 'ref_pg_mag', 'ref_proper_motion', 'ref_spect_type', 'remarks', 'ref_source_cat', 'num_source_cat', 'dm', 'hd', 'hd_component', 'gc', 'proper_motion_ra_fk5', 'proper_motion_dec_fk5', 'class']

    >>> datum = '''SAO 308|37.952962499999998|.18110000000000001|1|1908.0|89.264066670000005|-0.0040000000000000001|1|1902.5|.029999999999999999|123.28054164|26.461347790000001||2.1000000000000001|F8v|17|1|0|1|0|4|74|907|BD+88    8|8890|0|2243|.20119999999999999|-0.016|2480|'''
    >>> s = p.parse(datum)
    >>> s["name"]
    'SAO 308'
    >>> s["ra"] #doctest: +ELLIPSIS
    37.9529...

    """
    def __init__(self, f):
        self.d = {}
        line = f.readline()
        while not line.startswith("field["):
            line = f.readline()

        while line.startswith("field["):
            name, vspec = parse_valuespec(line)
            self.d[name] = vspec
            line = f.readline()

        while not line.startswith("line["):
            line = f.readline()
        self.items = line.split()[2:]

    def parse(self, line):
        xs = line.split('|')
        zs = zip(self.items, xs)
        d = {}

        for name, x in zs:
            vspec = self.d[name]
            #print name, x, vspec
            if x:
                v = vspec.parse(x)
                d[name] = v
            else:
                print >>sys.stderr, name, 'is empty, in ', d['name']
                d[name] = None
        return d


if __name__ == "__main__":
    import doctest
    doctest.testmod()

