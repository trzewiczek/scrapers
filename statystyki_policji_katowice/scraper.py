# coding: utf-8
try:
  from BeautifulSoup import BeautifulSoup as bs
except:
  from bs4 import BeautifulSoup as bs
from urllib import urlopen
from datetime import *
import codecs
import re
import json

f = codecs.open('result.csv', 'w', 'utf-8')

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

fields_order = [u'przestępstwa rozbójnicze', u'bójki i pobicia', u'kradzieże z włamaniem', u'kradzieże', u'wypadki', u'zabici', u'ranni', u'nietrzeźwi kierowcy', u'kolizje', u'policjanci interweniowali']

start_date = date(2008, 4,  1)
end_date   = date(2012, 9, 30)

header = u'"Data";%s\n' % u';'.join([u'"%s"' % e.title() for e in fields_order])
f.write(header)

d_re = re.compile(r'\d+')
for single_date in daterange(start_date, end_date):
    date = single_date.strftime("%Y_%m_%d")
    url  = 'http://www.slaska.policja.gov.pl/staystyka-zdarzen/go:data:%s' % date

    page = bs(urlopen( url ).read())
    tmp = {}
    for pos in page.findAll('div', 'sRow'):
      text = pos.text
      try:
        field = d_re.sub('', text).strip()
        value = d_re.findall(text).pop()
        tmp[field] = value
      except:
        pass

    
    print ">>> Saving: %s" % date
    date = date.replace('_', '-')
    data = u';'.join([ tmp.get(field, '') for field in fields_order ])
    row = '"%s";%s\n' % (date, data)
    f.write(row)

f.close()

