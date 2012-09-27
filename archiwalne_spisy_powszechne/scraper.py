from urllib import urlopen
from bs4 import BeautifulSoup as bs
import re

for i in range(9):
  base_url = 'http://statlibr.stat.gov.pl/F/QHISDYJ9TLR2DB3EAPJS1H99HMMKNEX76B1X1YGCC73L9HY88Q-33680?func=short-jump&jump=0000%s1' % i

  page = bs(urlopen(base_url).read())

  data_row = page.find_all('tr', {'valign': 'baseline'})[-1]

  title = data_row.find_all('td')[3]
  links = data_row.findAll('a', {'href': re.compile("MEDIA...$")})
 
  new_title = ''
  for letter in title.text.lower():
    if not letter.isalnum():
      new_title += '-'
    else:
      new_title += letter

  pat = re.compile(r'"([^"]+)"')
  for i,l in enumerate(links):
    popup_link = 'http://statlibr.stat.gov.pl' + pat.findall(l['href']).pop()
    popup = bs(urlopen(popup_link).read())
    pdf_link = pat.findall(popup.body['onload']).pop()
    print 'wget http://statlibr.stat.gov.pl%s %s-%s.pdf' % (pdf_link, new_title.strip('-'), i)
 
