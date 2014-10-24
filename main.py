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

    departments = ['statistics', 'mathematics', 'computer science', 'physics']
    search_keys = ['department faculty', 'faculty']

    for university in universities:

        university_id, university_name = university.university_id, university.name,
        university_region, university_url = university.region, university.url

        crawl_pages = page.Page(university_url, university_id)
        for department in departments:
            for search_key in search_keys:
                keywords = " ".join([university_name, department, search_key])
                print "[INFO] Searching: %s" % keywords
                search_results, search_next_link = search_util.bing_search(keywords, keys.bing_id, first_n=5)
                for result_object in search_results:
                    crawl_pages.crawl_node(result_object.url, 0) #currently scrape depth 0, only surface
                    professor_list = crawl_pages.output_professors()
                    db_util.insert_professors(professor_list)
        #pdb.set_trace()

        #break



