import requests
from bs4 import BeautifulSoup
import csv

from scraper_util import *

if __name__ == '__main__':
    csv_out = csv.writer(open("universities.csv", "a"))
    csv_out.writerow(["UNIVERSITY", "URL", "STATE"])
    start = 1
    while start < 2100:
        raw_html = getRawHtml("http://univ.cc/search.php?dom=edu&key=&start=%s" % start)
        bs_struct = BeautifulSoup(raw_html, "html.parser")
        for institution in bs_struct.find_all('li'):
            links = institution.find_all('a', href=True)
            if len(links) != 0:
                link = links[0]
                university_name = link.text.encode('utf-8')
                url = link['href'].encode('utf-8')
                csv_out.writerow([university_name, url])
        start += 50






