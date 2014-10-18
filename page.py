from bs4 import BeautifulSoup, SoupStrainer
import requests

from scraper_util import *

import re
import sets

class Page(object):


    media_extensions = ['mp3']
    text_extensions = ['doc']


    def __init__(root_url, uid):
        self.root_url = root_url
        self.uid = uid
        self.emails = {}
        self.crawled_links_set = Set()

    def crawl_root(depth=1):
        crawl_node(self.root_url, depth)

    def crawl_node(entry_node_link, depth=1):
        #starts crawling from the entry_node_link, goes up to depth 1. Doesn't revisit ones we've seen.
        if depth == 0:
            extract_new_links

        crawl_node(entry_node_link, depth-1)


    def extract_new_links(page):
        '''
        Extracts all new links from the page.
        Won't return links visited before.
        '''
        #page =

    def link_worth_visit(link):
        '''
        Returns true if we're going to visit the link.
        '''
        !is_media_link(link) and !is_text_link(link)

    def is_media_link(link):
        return !has_extension(media_extensions, link)

    def is_text_link(link):
        return !has_extension(text_extensions, link)

    def has_extension(taboo_list, link):
        resource = link.replace(root_url, "")
        for taboo in taboo_list:
            if taboo in resource:
                return True
        return False

    #################
    ###### Exit #####
    #################
   def output():
       #output the university set.
       pass


