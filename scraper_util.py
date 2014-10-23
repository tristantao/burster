import requests
from bs4 import BeautifulSoup

class PageError(RuntimeError):
   def __init__(self, msg):
      self.msg = msg

def getRawHtml(raw_link):
    #Givne a raw link, queries and returns the raw html
    print "[STATUS] Scraping {0}".format(raw_link)
    r = requests.get(raw_link)
    if(r.status_code != requests.codes.ok):
        print "WARN: Request did not come back with OK status code for: %s \nExiting" % raw_link
        raise PageError("Bad Request")
    raw_html = r.text
    return raw_html
