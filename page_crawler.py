import sys
import time, csv, optparse
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import date
import re

from scraper_util import *

from pygoogle import pygoogle
import math

def google_search(keywords, first_n):
    #given a keywords, returns the link to first_n results.
    cleaned_keywords = re.sub( '\s+', ' ', keywords)
    required_pages = math.ceil(first_n / 8.0)
    g = pygoogle(cleaned_keywords)
    g.pages = int(required_pages)
    result_links = g.get_urls()
    return result_links[:first_n]


