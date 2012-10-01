# coding: utf-8
from BeautifulSoup import BeautifulSoup as bs
from urllib import urlopen
from datetime import *
import codecs

f = codecs.open('result.csv', 'w', 'utf-8')

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2008, 4,  1)
end_date   = date(2012, 9, 30)

header = u'"Data";"Przestępstwa rozbójnicze";"Bójki i pobicia";"Kradzieże z włamaniem";"Kradzieże";"Wypadki";"Zabici";"Ranni";"Nietrzeźwi kierowcy";"Kolizje";"Policjanci interweniowali"\n'
f.write(header)

for single_date in daterange(start_date, end_date):
    date = single_date.strftime("%Y_%m_%d")
    url  = 'http://www.slaska.policja.gov.pl/staystyka-zdarzen/go:data:%s' % date

    page = bs(urlopen( url ).read())
    data = page.findAll('span', 'sIlosc')

    print ">>> Saving: %s" % date
    row = '"%s";%s\n' % (date.replace('_', '-'), u';'.join([ e.text for e in data ]))
    f.write(row)

f.close()

