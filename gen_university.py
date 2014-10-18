import requests
from bs4 import BeautifulSoup
import csv

def getRawHtml(raw_link):
    #Givne a raw link, queries and returns the raw html
    print "[STATUS] Scraping {0}".format(raw_link)
    r = requests.get(raw_link)
    if(r.status_code != requests.codes.ok):
        print "WARN: Request did not come back with OK status code for: %s \nExiting" % raw_link
        exit(1)
    raw_html = r.text
    return raw_html

raw_html = getRawHtml("http://www.utexas.edu/world/univ/alpha/")
bs_struct = BeautifulSoup(raw_html, "html.parser")
csv_out = csv.writer(open("universities.csv", "a"))
csv_out.writerow(["UNIVERSITY", "URL", "STATE"])
#csv_out.writerow(["Name","Address","Telephone","Fax","E-mail","Others"])

#for university_box in bs_struct.find_all('div', {"class": "box2l"}):

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





