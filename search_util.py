import sys
import time, csv, optparse, random
from bs4 import BeautifulSoup, SoupStrainer
import requests
from datetime import date
import re
from itertools import islice, cycle
from nltk.tokenize import word_tokenize
import nltk
import HTMLParser

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

def web_searh(search_word, limit=10):
    #Retrusna a list of Result objects
    #the actual search function caled by other functions.
    bing = PyBingSearch(keys.bing_id)
    result_list, next_page = bing.search(search_word, limit, format='json') #email + " " + school
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
            return self.root.string if self.root.string != None else ""

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
    #Returns a tuple of (name, score)
    raw_html = getRawHtml(page)
    name = email.split("@")[0] if "@" in email else email #@TODO check if including the @ makes the search better (or try both)
    name = sorted(re.split('\.|\_|\-', name), key=lambda c: len(c), reverse=True)[0]
    #@TODO take care when it is [at] or [dot]. Currently ignoring it by not looking for '@'.

    try:
        bs_struct = BeautifulSoup(raw_html, "html.parser")
    except HTMLParser.HTMLParseError as hPE:
        print str(hPE)
        return None
    name_regex = r'' + re.escape(name)
    candidates = {}
    if len(bs_struct(text=re.compile(name_regex))) != 0:
        elem = bs_struct(text=re.compile(name_regex))[0]
        elem =  elem.parent
        element_prev_iterable_token = IterableElementToken(elem, "previous")
        element_next_iterable_token = IterableElementToken(elem, "next")

        for index, search_element in enumerate(roundrobin(element_prev_iterable_token, element_next_iterable_token)):
            try:
                tokenized_encoded_element = word_tokenize(search_element.encode('utf8'))
                if len(tokenized_encoded_element) != 0 and all([(encoded_element_token[0].isupper() and len(encoded_element_token) > 0) for encoded_element_token in tokenized_encoded_element if encoded_element_token.isalpha()]):
                    tokenized_encoded_element_scores = [nltk.metrics.edit_distance(name, t.lower()) + (index / 10.0) for t in tokenized_encoded_element]
                    candidates[tuple(tokenized_encoded_element)] = min(candidates.get(tuple(tokenized_encoded_element), sys.maxint), min(tokenized_encoded_element_scores))
                    print "%s  : %s" % (tuple(tokenized_encoded_element), tokenized_encoded_element_scores)
            except RuntimeError as rE:
                #encode sometimes gets into an infinite recursion for some reason.
                continue
                print str(rE)
                return None
    else:
        print "[INFO] Email Name '%s' NOT found in page '%s'. Continuing." % (email, page)
    try:
        extracted_name_score_token = sorted(candidates.iteritems(), key=lambda k: k[1])[0]
        return extracted_name_score_token
    except IndexError as iE:
        return None

def name_from_email(email, school_name, first_n=3):
    # Grabs the professor's name from bing. Need to better leverage the resulting html.
    # @TODO refactor to shorten function
    try:
        local_part = email.lower().split("@")[0]
    except IndexError as iE:
        print "[ERROR] Bad email: %s" % email
        return None
    #search_word = " " + email + " " + school_name
    search_word = email
    result_list = web_searh(search_word, limit=10)

    #first pass uses html source
    source_level_extraction_results = []
    for result_index, result in enumerate(result_list):
        if result_index <= 3:
            extracted_name_score_token = page_name_extraction(result.url, email)
            if extracted_name_score_token:
                source_level_extraction_results.append(extracted_name_score_token)
        else:
            break
    try:
        source_level_extraction_results = sorted(source_level_extraction_results, key=lambda (x,y): y)
    except TypeError as tE:
        print "WARN: could not complete full sort due to bad extractions"
        source_level_extraction_results = []

    #2nd pass uses title matching
    result_page_tokenization_search_result = ""
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
                result_page_tokenization_search_result = token.title()

    #3rd pass - counts tokenes
    title_hashes = {}
    for result_index, result in enumerate(result_list):
        print result.title
        for token in [t for t in re.split('[^a-zA-Z]', result.title) if t != '']:
            token = token.lower()
            title_hashes[token] = title_hashes.get(token, 0) + 1
    token_counter_result = sorted(title_hashes.iteritems(), key=lambda (x, y): y, reverse=True)[0:5]
    print token_counter_result

    if len(source_level_extraction_results) != 0:
        try:
            print '*' * 100 + "SRC level extrated for %s:" % email
            print " ".join(source_level_extraction_results[0][0])
            return " ".join(source_level_extraction_results[0][0])
        except Exception as e:
            print "[ERR] Failed to extract %s. Printing source_level_extraction_results below" + email
            print source_level_extraction_results
    elif result_page_tokenization_search_result:
        return result_page_tokenization_search_result
    else:
        print "Token Counter:"
        print token_counter_result

    #print result_page_tokenization_search_result
    #print token_couter_result
    return None


#page_name_extraction(page, email)

#name_from_email("anirbanb@stat.tamu.edu", "Texas A&M University", bing_id=keys.bing_id)
#name_from_email("negativetwelve@gmail.com", "")
#name_from_email("massellol@walshjesuit.org", "Walsh University")

#name_from_email("dcline@stat.tamu.edu", "", bing_id=keys.bing_id)
#name_from_email("sattar@bard.edu", "Bard College")
name_from_email("pmerrill@wingate.edu", "Wingate University")


#
#name_from_email("lane@bard.edu", "Bard College")
#mhandelm@bard.edu
#print page_name_extraction('http://www.gradschool.usciences.edu/faculty/walasek-carl', 'c.walase@usciences.edu')









