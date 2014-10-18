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
        self.crawled_links_set = set()

    def crawl_root(depth=1):
        crawl_node(self.root_url, depth)

    def crawl_node(entry_node_link, depth=1):
        '''
        Starts crawling from the entry_node_link, goes down to depth 1.
        Doesn't revisit ones we've seen.
        '''
        extract_info(entry_node_link)
        if depth != 0:
            for neighboring_link in extract_new_target_links(entry_node_link):
                crawl_node(neighboring_link, node-1)

    def extract_info(link):
        '''
        Extracts the relevant info from the link.
        Updates the instance vars.
        '''

        pass

    def extract_new_target_links(link):
        '''
        Extracts all new links from the page.
        Won't return links visited before.
        Only returns links that pass the rules to visit.
        '''
        target_links = set()
        raw_html = getRawHtml(link)
        bs_struct = BeautifulSoup(raw_html, "html.parser")
        for potential_link in bs_struct.find_all('a', href=True):
            link_href = potential_link['href']
            if (link_href not in crawled_links_set) and should_visit(link_href):
                target_links.add(potential_link['href'])
                crawled_links_set.add(target_links)
        return target_links

    def should_visit(link):
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


