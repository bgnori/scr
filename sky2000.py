
import I239

f = open('sky2000-text.description')

parser = I239.ParserBuilder(f.read())
f.close()

print parser.properties

line = """SKY2000 J235957.13-200209.723590199224691  192302 SD-20 6687                       275561                             235957.1316-20 2 9.7730.0293 65+0.00462-00.008265        +0.005100.0171  68 0.939477-0.000196-0.342611 61.27-76.25 9.50      0.026 68 10.36 +0.8550.037 68                     9.4 210.5 2G8IV                          23G5  2                                 0.1123 0.1123"""

e = parser.parse(line)
print e["SKY2000"]
print e["RAh"], e["RAm"], e["RAs"]
print e["DE-"], e["DEd"], e["DEm"], e["DEs"]
