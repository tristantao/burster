import requests
from bs4 import BeautifulSoup
import csv

from scraper_util import *

if __name__ == '__main__':
    raw_html = getRawHtml("http://www.utexas.edu/world/univ/alpha/")
    bs_struct = BeautifulSoup(raw_html, "html.parser")
    csv_out = csv.writer(open("universities.csv", "a"))
    csv_out.writerow(["UNIVERSITY", "URL", "STATE"])

    for institution in bs_struct.find_all('li'):
        state = institution.text.encode('utf-8')
        links = institution.find_all('a', href=True)
        link = links[0]
        url = link['href'].encode('utf-8')
        university = link.text.encode('utf-8')
        state = state.replace(university, "")
        #print url
        #print university
        #print state
        csv_out.writerow([university, url, state])





