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
    def parse(self, line):
        pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()

