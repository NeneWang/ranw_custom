import csv
with open(r'D:\ANR24\HCap\Hculture\bisearch\HCulture43bi.csv') as e:
    dreader = csv.reader(e)
    hpdic = list(dreader)
data = [i[0] for i in hpdic]