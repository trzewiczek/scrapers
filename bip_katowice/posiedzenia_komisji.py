# coding: utf-8
from bs4 import BeautifulSoup as bs
import urllib
import re

re_date = re.compile(ur'(\d{1,2}[\. ]+\w+[\. ]+\d{4}\s*r?\b)', re.UNICODE)

base_url = 'http://bip.um.katowice.pl/%s'
groups = {
    'index.php?s=20&id=1292316724': u'Budżetu miasta',
    'index.php?s=20&id=1292316788': u'Edukacji',
    'index.php?s=20&id=1292317193': u'Infrastruktury i środowiska',
    'index.php?s=20&id=1292316878': u'Kultury, promocji i sportu',
    'index.php?s=20&id=1292316610': u'Organizacyjna',
    'index.php?s=20&id=1292316948': u'Polityki społecznej',
    'index.php?s=20&id=1292316485': u'Rewizyjna',
    'index.php?s=20&id=1292317310': u'Rozwoju miasta'              
}
tmpl = {
   u'Budżetu miasta': 0,          
   u'Edukacji': 0,
   u'Infrastruktury i środowiska': 0,
   u'Kultury, promocji i sportu': 0,
   u'Organizacyjna': 0,
   u'Polityki społecznej': 0,
   u'Rewizyjna': 0,
   u'Rozwoju miasta': 0
}
months = {
    u'stycznia'    : u'.01.',
    u'lutego'      : u'.02.',
    u'marca'       : u'.03.',
    u'kwietnia'    : u'.04.',
    u'maja'        : u'.05.',
    u'czerwca'     : u'.06.',
    u'lipca'       : u'.07.',
    u'sierpnia'    : u'.08.',
    u'września'    : u'.09.',
    u'października': u'.10.',
    u'listopada'   : u'.11.',
    u'grudnia'     : u'.12.'
}

dates = []
results = {}

for url, group in groups.items():
    page = bs(urllib.urlopen(base_url % url).read())
    part = page.find_all('div', 'tresc_l')[-1]

    for li in part.find_all('li'):
        txt  = li.text
        date = re_date.findall(txt)[0].strip(u' r.')

        for m, n in months.items():
            date = date.replace(m, n)
        date = date.strip().replace(u' ', u'')
        date = u"%s.%s" % (date[-4:], date[-7:-5])

        results.setdefault(date, dict(tmpl))
        results[date][group] += 1

        dates.append(date)

final_data = []
for y in range(2010, 2013):
    for m in range(1, 13):
        mm = u'0%s' % m if m < 10 else u'%s' % m
        date = u'%s.%s' % (y, mm)

        monthly = results.get(date, dict(tmpl))
        nums = [ monthly[group] for group in sorted(monthly.keys()) ]
        final_data.append(nums)

        print u'%s;%s;%s;%s;%s;%s;%s;%s' % tuple(nums)

from pylab import *
pcolor(array(final_data), cmap=cm.Greens)
show()



Budżetu miasta
Edukacji
Infrastruktury i środowiska
Kultury, promocji i sportu
Organizacyjna
Polityki społecznej
Rewizyjna
Rozwoju miasta

