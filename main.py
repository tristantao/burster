#standard imports
import sys
import time, csv, optparse
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import date

import pdb

#util imports
import db_util
import search_util
import page
import keys

if __name__ == '__main__':
    universities = db_util.get_university_from_db()

    departments = ['statistics', 'mathematics', 'computer science']
    search_keys = ['department faculty', 'career']

    for university_name, university_url in universities.iteritems():
        page = page.Page(university_url, university_name)
        for department in departments:
            for search_key in search_keys:
                keywords = " ".join([university_name, department, search_key])
                search_results, search_next_link = search_util.bing_search(keywords, keys.bing_id, first_n=5)
                for result_object in search_results:
                    page.crawl_node(result_object.url, 1)
        pdb.set_trace()
        page.output()
        #break



