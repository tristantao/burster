from bs4 import BeautifulSoup, SoupStrainer
import requests

from scraper_util import *

import re
import sets

class Page(object):

    def __init__(university_url, university_name):
        self.university_url = university_url
        self.university_name = university_name
        self.emails = {}
        self.crawled_links_set = Set()

    def crawl_root(root_link, depth=1):
        #starts crawling from the root, goes up to depth 1. Doesn't revisit ones we've seen.
        pass


   def output():
       #output the university set.
       pass