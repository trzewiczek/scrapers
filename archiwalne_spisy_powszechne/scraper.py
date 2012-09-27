from bs4 import BeautifulSoup as bs
from urllib import urlopen
import codecs
import re

f = codecs.open('download.sh', 'w', 'utf-8')

for i in range(9):
  base_url = 'http://statlibr.stat.gov.pl/F/QHISDYJ9TLR2DB3EAPJS1H99HMMKNEX76B1X1YGCC73L9HY88Q-33680?func=short-jump&jump=0000%s1' % i

  page = bs(urlopen(base_url).read())
  data_rows = page.find_all('tr', {'valign': 'baseline'})

  for data_row in data_rows:
    title = data_row.find_all('td')[3]
    # there are multiple pdfs for a single table entry
    links = data_row.findAll('a', {'href': re.compile("MEDIA...$")})
   
    # slugify the title
    new_title = ''
    for letter in title.text.lower():
      if not letter.isalnum():
        new_title += '-'
      else:
        new_title += letter

    # intermediate url extraction regex
    pat = re.compile(r'"([^"]+)"')
    for i,l in enumerate(links):
      # the real pdf links are present in the body attribute of the popup window
      popup_link = 'http://statlibr.stat.gov.pl' + pat.findall(l['href']).pop()
      popup = bs(urlopen(popup_link).read())

      # final pdf link extracted from the popup window
      pdf_link = pat.findall(popup.body['onload']).pop()

      # collect results as wget commands with an entry title as a filename
      f.write(u'wget http://statlibr.stat.gov.pl%s %s-%s.pdf\n' % (pdf_link, new_title.strip('-'), i))

f.close()
