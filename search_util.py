import sys
import time, csv, optparse, random
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import date
import re
from itertools import islice, cycle
from nltk.tokenize import word_tokenize
import nltk

from scraper_util import *


from pygoogle import pygoogle
from pybingsearch import PyBingSearch

import keys

import math
import pdb

def google_search(keywords, first_n):
    #given a keywords, returns the link to first_n results.
    #@Deprecated by a long shot
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

def web_searh(search_word):
    #Retrusna a list of Result objects
    #the actual search function caled by other functions.
    bing = PyBingSearch(keys.bing_id)
    result_list, next_page = bing.search(search_word, limit=10, format='json') #email + " " + school
    return result_list

class IterableElementToken:
    def __init__(self, starting_node, direction):
        # starting_node is a beautiful soup page element.
        # direction has to be 'next' or 'previous'
        self.root = starting_node
        if direction == "previous" or direction == "next":
            self.direction = direction
        else:
            raise Exception("Bad Direction")

    def __iter__(self):
        return self

    def next(self):
        self.root = self.root.previous_element if self.direction == "previous" else self.root.next_element
        if self.root == None:
            raise StopIteration
        else:
            return self.root

def roundrobin(*iterables):
    #Given a series of iterables, it'll iterate via roundrobin for all.
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def page_name_extraction(page, email):
    #Given a page and an email, retuns a string that is most likely the name of the email
    raw_html = getRawHtml(page)
    name = email.split("@")[0] if "@" in email else email #@TODO check if including the @ makes the search better (or try both)
    name = sorted(re.split('\.|\_|\-', name), key=lambda c: len(c), reverse=True)[0]
    #@TODO take care when it is [at] or [dot].

    bs_struct = BeautifulSoup(raw_html, "html.parser")
    name_regex = r'' + re.escape(name)
    candidates = {}
    for elem in bs_struct(text=re.compile(name_regex)):
        elem =  elem.parent
        element_prev_iterable_token = IterableElementToken(elem, "previous")
        element_next_iterable_token = IterableElementToken(elem, "next")

        for index, search_element in enumerate(roundrobin(element_prev_iterable_token, element_next_iterable_token)):
            tokenized_encoded_element = word_tokenize(search_element.encode('utf8'))
            if len(tokenized_encoded_element) != 0 and all([encoded_element_token[0].isupper() for encoded_element_token in tokenized_encoded_element]):
                tokenized_encoded_element_scores = [nltk.metrics.edit_distance(name, t.lower()) for t in tokenized_encoded_element]
                candidates[tuple(tokenized_encoded_element)] = min(tokenized_encoded_element_scores)
                #print tokenized_encoded_element + tokenized_encoded_element_scores
            #if encoded_element[0].isupper(): #only check upper
                #print search_element.encode('ascii','ignore')
    try:
        extracted_name_token = sorted(candidates.iteritems(), key=lambda k: k[1])[0]
        return extracted_name_token
    except IndexError as iE:
        return None

def name_from_email(email, school_name, first_n=3):
    #Grabs the professor's name from bing. Need to better leverage the resulting html.
    try:
        local_part = email.lower().split("@")[0]
    except IndexError as iE:
        print "[ERROR] Bad email: %s" % email
        return None
    search_word = "professor. " + email + ' ' + school_name
    result_list = web_searh(search_word, limit=10)

    #first pass
    for result_index, result in enumerate(result_list):
        if result_index < 4:
            print page_name_extraction(result.url, email)
        else:
            break
        continue

    #2nd pass
    for result_index, result in enumerate(result_list):
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


#page_name_extraction(page, email)

#name_from_email("anirbanb@stat.tamu.edu", "Texas A&M University", bing_id=keys.bing_id)
name_from_email("massellol@walshjesuit.org", "Walsh University", bing_id=keys.bing_id)
#name_from_email("dcline@stat.tamu.edu", "", bing_id=keys.bing_id)


#print page_name_extraction('http://www.gradschool.usciences.edu/faculty/walasek-carl', 'c.walase@usciences.edu')









