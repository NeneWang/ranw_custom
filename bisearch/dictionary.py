import csv
# with open(r'D:\ANR24\HCap\Hculture\bisearch\HCulture43bi.csv') as e:
with open('./hciknoheader.csv') as e:
    dreader = csv.reader(e)
    hpdic = list(dreader)
    # bisearch/hciknoheader.csv
# print('First in data', data[:10])
data = [i[0] for i in hpdic]
