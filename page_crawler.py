import sys
import time, csv, optparse
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import date
import re

from scraper_util import *

from pygoogle import pygoogle
from pybing import Bing
from bingsearch import BingSearch

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

def bing_search(keywords, bing_id, first_n=50):
    #does a Bing search given a keyword
    bing = BingSearch(bin_id)
    return bing.search(keywords, limit=first_n, format='json')


def name_from_email(email, school, first_n=3):
    local_part = email.lower().split("@")[0]
    search_word = "professor. " + email + ' ' + school
    g = pygoogle(search_word)
    g.pages = first_n
    res = g.search()
    pdb.set_trace()
    for (title, link) in res.iteritems():
        tokenized_names = title.lower().split()
        n_gram = ""
        for token in tokenized_names:
            n_gram += (token + " ")
            if token in local_part:
                return token
                #return n_gram
    return None


#name_from_email("anirbanb@stat.tamu.edu", "Texas A&M University")
#name_from_email("dcline@stat.tamu.edu", "")



