
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

>>> entry = parser.parse(line)
>>> entry.HIP
1

>>> entry.RAhms
'00 00 00.22'

>>> entry.DEdms
'+01 05 20.4'
'''

class Entry:
    def __init__(self):
        self.HIP = 1
        self.RAhms = '00 00 00.22'
        self.DEdms = '+01 05 20.4'

class Parser:
    def __init__(self, description):
        xs = description.splitlines()
        self.name = xs[0][len("Byte-by-byte Description of file: "):]

        self.properties = [{}, {}, {}, {"Label":"RAhms", "Explanations":'Right ascension in h m s, ICRS (J1991.25) (H3)'}]
        pass
    def __getitem__(self, key):
        assert isinstance(key, int)
        return self.properties[key]

    def parse(self, line):
        return Entry()



def ParserBuilder(description):
    return Parser(description)


if __name__ == "__main__":
    import doctest
    doctest.testmod()


