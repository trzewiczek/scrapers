# coding: utf-8
import logging
from bs4 import BeautifulSoup as bs
from urllib import urlopen
import re


def scrape_articles(page):
    articles = page.find(id='holder_213').find_all('h3')
      
    archive = []
    for article in articles:
        link_tag = article.find('a')
        art_link = link_tag['href'].split('url=').pop().encode('utf-8') 

        if art_link.startswith('http://www.tokfm.pl/Tokfm'):
            art_page = bs(urlopen(art_link).read())

            lead = art_page.find(id='gazeta_article_lead').text
            body = art_page.find(id='artykul').text.strip().replace('        ', '\n')

            date = art_page.find(id='gazeta_article_date').text
            date = date.split(',')[0].strip()

            tmp = {
              'title' : article.text.strip(),
              'text'  : lead + '\n' + body,
              'date'  : date,
              'author': art_page.find(id='gazeta_article_author').text
            }
            archive.append(tmp)

            logging.info("Archived: %s" % tmp['title'])
        else:
            logging.warning("%s" % art_link)

    return archive


def scrape_blogs(page):
    articles = page.find('ul', 'entries').find_all('h2')

    archive = []
    for article in articles:
        art_link = 'http://tokfm.pl%s' % article.find('a')['href']
        art_page = bs(urlopen(art_link).read())

        header = art_page.find(id='BL_bloxHead')
        author = header.find('h2').find('a').text

        post = art_page.find(id='BL_entries')
        try:
            body = post.find('div', 'body').text.strip()
        except AttributeError:
            body = ''
        date = post.find('p', 'date').text.strip().split()[0]

        tmp = {
          'title' : article.text.strip(),
          'text'  : body,
          'date'  : date,
          'author': author
        }
        archive.append(tmp)

        logging.info("Archived: %s" % tmp['title'])

    return archive

    
if __name__ == '__main__':
    todo = [
      ('http://www.tokfm.pl/Tokfm/0,103087.html', scrape_articles),
      ('http://www.tokfm.pl/Tokfm/0,103085.html', scrape_articles),
      ('http://www.tokfm.pl/Tokfm/0,103089.html', scrape_articles),
      ('http://www.tokfm.pl/blogi', scrape_blogs)
    ]

    archive = []
    for url, scrape in todo:
      page     = bs(urlopen(url).read())
      archive += scrape(page)

    print "W sumie %s artykułów." % len(archive)

    # TODO save uniques to db
