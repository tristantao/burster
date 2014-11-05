import sys
import time, csv, optparse, random
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import date
import re

from scraper_util import *

from pygoogle import pygoogle
from pybingsearch import PyBingSearch

import keys

import math
import pdb

def google_search(keywords, first_n):
    #given a keywords, returns the link to first_n results.
    cleaned_keywords = re.sub( '\s+', ' ', keywords)
    required_pages = math.ceil(first_n / 8.0)
    g = pygoogle(cleaned_keywords)
    g.pages = int(required_pages)
    result_links = g.get_urls()
    return result_links[:first_n]

def bing_search(keywords, bing_id, first_n=50, throttle=True):
    #does a Bing search given a keyword
    print "[STATUS] PyBingSearching {0}".format(keywords)
    if throttle:
        time.sleep(random.random())
    try:
        bing = PyBingSearch(bing_id)
        search_result, next_link = bing.search(keywords, limit=first_n, format='json')
    except pybingsearch.PyBingException as pBE:
        print str(pBE)
        sys.exit(1)
    return search_result, next_link

def name_from_email(email, school_name, bing_id, first_n=3):
    #Grabs the professor's name from bing. Need to better leverage the resulting html.
    try:
        local_part = email.lower().split("@")[0]
    except IndexError as iE:
        print email
        return None
    search_word = "professor. " + email + ' ' + school_name
    bing = PyBingSearch(bing_id)
    ressult_list, next_page = bing.search(search_word, limit=50, format='json') #email + " " + school
    for result in ressult_list:
        title, link = result.title, result.url
        #tokenized_names = title.lower().split()
        tokenized_names = re.findall(r"\w+", title.lower())
        n_gram = ""
        for token in tokenized_names:
            if len(token) < 3:
                continue
            n_gram += (token + " ")
            if token in local_part:
                return token.title()
    return None


#name_from_email("anirbanb@stat.tamu.edu", "Texas A&M University", bing_id=keys.bing_id)
print name_from_email("rmclaughlin@walsh.edu", "Walsh University", bing_id=keys.bing_id)

#name_from_email("dcline@stat.tamu.edu", "")



