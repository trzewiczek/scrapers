# coding: utf-8
from BeautifulSoup import BeautifulSoup as bs
from urllib import urlopen
from datetime import *
import codecs

f = codecs.open('czujniki.csv', 'w', 'utf-8')

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2008, 12, 30)
end_date   = date(2012,  9, 26)

f.write(u'"Miejscowość";"Ulica";"Data";"Godzina";"Dwutlenek siarki (SO2) (μg/m3)";"Tlenek azotu (NO) (μg/m3)";"Dwutlenek azotu (NO2) (μg/m3)";"Tlenek węgla (CO) (średnie ośmiogodz.) (mg/m3)";"Ozon (O3) (średnie jednogodz.) (μg/m3)";"Ozon (O3) (średnie ośmiogodz.) (μg/m3)";"Tlenki azotu (NOx) (μg/m3)";"Pył zawieszony (PM10) (μg/m3)";"Prędkość wiatru (WS) (m/s)";"Kierunek wiatru (WD) (o(stopnie))";"Ciśnienie atmosferyczne (PA) (hPa)";"Temperatura (TP) (°C)";"Wilgotność (%)";"Ilość opadu (mm)";"Promieniowanie słoneczne całkowite (W/m2)";"Prom UVB - efektywny strumień W/m2 (W/m2)";"Benzen (C6H6) (μg/m3)";"Ksylen  (C8H10) (μg/m3)";"Toluen (C7H8) (μg/m3)";"M-P-ksylen (C8H10) (μg/m3)"\n')

locations = {
    "bielskobiala_ko": u"Bielsko-Biała, ul. Kossak-Szczuckiej 19",
    "cieszyn": u"Cieszyn, ul. Mickiewicza 13",
    "czestochowa_ak": u"Częstochowa, Al. Armii Krajowej 3",
    "czestochowa_ba": u"Częstochowa, ul. Baczyńskiego 2",
    "dabrowagorn_ty": u"Dąbrowa Górnicza, ul. Tysiąclecia 25a",
    "gliwice_me": u"Gliwice, ul. Mewy 34",
    "godow": u"Godów, ul. Gliniki",
    "katowice_a4": u"Katowice, autostrada A4, ul. Górnośląska/Plebiscytowa",
    "katowice_ko": u"Katowice, ul Kossutha 6",
    "rybnik_bo": u"Rybnik, ul. Borki 37a",
    "sosnowiec_lu": u"Sosnowiec, ul. Lubelska 51",
    "tychy": u"Tychy, ul. Tołstoja 1",
    "ustron": u"Ustroń, Sanatoryjna 7",
    "wodzislaw": u"Wodzisław, Gałczyńskiego 1",
    "zabrze": u"Zabrze, ul. Skłodowskiej-Curie 34",
    "zlotypotok": u"Złoty Potok, leśniczówka Kamienna Góra",
    "zory": u"Żory, ul. Sikorskiego 52",
    "zywiec_sl": u"Żywiec, ul. Słowackiego 2"
}
for location in sorted(locations.keys()):
  city, address = locations[location].split(', ', 1)

  for single_date in daterange(start_date, end_date):
      url =  'http://stacje.katowice.pios.gov.pl/monitoring/raport6.php'
      url += '?wybor_st_pa=stacja&tryb=aut&rodzaj=dzienny&stacja=%s'
      url += '&parametr=&data=%s' 

      table = bs(urlopen( url % (location, single_date) ).read())

      data_rows = table.find('table').findAll('tr', 'parametr')
      data_table = [[cell.text for cell in row.findAll('td')[3:]] for row in data_rows]

      new_table = [["" if e[i] == u'-' else e[i].replace(',', '.') for e in data_table] for i in range(len(data_table[0]))]

      for h, row in enumerate(new_table):
        f.write('"%s";"%s";"%s";"%s:00";%s\n' % (city, address, single_date, h+1 if h >=9 else '0'+str(h+1), ';'.join(row)))

f.close()

