#!/usr/bin/env python2
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import csv
from glob import glob
from bs4 import BeautifulSoup
from collections import OrderedDict

OUT = open('stores.txt','w')
CSV = csv.writer(open('stores.csv','w'))
ERR = open('stores.err', 'w')
print "Writing to output file 'stores.txt'"

def output(store):
    for field, value in store.items():
        print>>OUT, "%s: %s" % (field, value)
    row = [value for value in store.values()]
    CSV.writerow(row)

def clean(s):
    return " ".join(s.split())

for fname in glob('html/*.html'):
    html = open(fname).read()
    soup = BeautifulSoup(html)
    store = OrderedDict()
    basename = fname.replace('html/','').replace('.html','')
    store['code'] = basename
    try:
        store['Split'] = soup.title.string.split('(')[0]
        ownership = soup.title
        print "Extracting from:", fname
    except Exception as e:
        print "Skipping empty:", fname
        continue
    
    store['owner'] = soup.find('h1', {'class':'fichePmIdentDeno'}).text
    siretnum = soup.find('span', {'class':'ficheNumSiren'}).text
    store['ownerSiret'] = siretnum
    postal =  html.find("codePostal")
    postalcode = html[postal + 12:postal + 17]
    store['zip'] = postalcode
    cityloc =  html.find("bureauDistributeur:")
    city = html[cityloc + 20:cityloc + 50]
    city = city.split('"')[0]
    store['city'] =  city
    store['zip'] = postalcode
    soup2 =soup.find("td", class_="first")
    address  = soup2.h3.next_sibling
    store['address'] = address
    estab = html.find("nbEtablissements:")
    establishments = html[estab + 17: estab +20]
    establishments = establishments.split(",")[0]
    store['storecount'] = establishments
    last = html.find("annee:")
    lastyear = html[last+6:last+10]
    store['year'] = lastyear

    output(store)
    print>>OUT, "----"
