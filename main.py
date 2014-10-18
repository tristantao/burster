import sys
import time, csv, optparse
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import date

from gen_university import *

if __name__ == '__main__':
    universities = 'university.csv'
    departments = ['statistics', 'mathematics', 'computer science']
    search_keys = ['department faculty', 'career', '']
    google_search_word = "https://www.google.com/?gws_rd=ssl#q=%s"

