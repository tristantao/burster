import sys
import time, csv, optparse
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import date

#from page_crawler import *
#from scraper_util import *

from page import *

if __name__ == '__main__':
    universities = 'university.csv'
    departments = ['statistics', 'mathematics', 'computer science']
    search_keys = ['department faculty', 'career', '']


    for university_entry in universities:
        university_page = Page("university_entry")
        for department in departments:
            for search_key in search_keys:
                keywords = " ".join(university_entry, department, search_key)
                search_result = google_search(keywords, 4)
                for result_link in search_result:
                    page.crawl_root(result_link, 1)
        page.output()

