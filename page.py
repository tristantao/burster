import re
import time
import random
import sets
import urlparse
from bs4 import BeautifulSoup, SoupStrainer
import requests

from scraper_util import *
import professor

import pdb

class Page(object):

    media_extensions = ['mp3', 'jpg', 'png']
    text_extensions = ['doc', 'pdf']
    email_regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                              "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                              "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

    def __init__(self, root_url, university_id):
        self.root_url = root_url
        self.university_id = university_id
        self.emails = set()
        self.crawled_links_set = set()

    def crawl_root(self, depth=1):
        self.crawl_node(self.root_url, depth)


    def crawl_node(self, entry_node_link, depth=1):
        '''
        Starts crawling from the entry_node_link, goes down to depth 1.
        Doesn't revisit ones we've seen.
        '''
        try:
            link_html = getRawHtml(entry_node_link)
        except PageError as e:
            print e.msg
            return
        self.extract_info(link_html)
        if depth != 0:
            for neighboring_link in self.extract_new_target_links(link_html):
                time.sleep(random.random()/5)
                self.crawl_node(neighboring_link, depth=depth-1)

    def get_emails(self, s):
        '''
        @author dideler@github
        Returns an iterator of matched emails found in string s.
        '''
        # Removing lines that start with '//' because the regular expression
        # mistakenly matches patterns like 'http://foo@bar.com' as '//foo@bar.com'.
        return ([email[0] for email in re.findall(self.email_regex, s) if not email[0].startswith('//')])

    def extract_info(self, link_html):
        '''
        Extracts the relevant info from the link.
        Updates the instance vars.
        '''
        for email in self.get_emails(link_html):
            self.emails.add(email)
        #pdb.set_trace()

    def extract_new_target_links(self, link_html):
        '''
        Extracts all new links from the page.
        Won't return links visited before.
        Only returns links that pass the rules to visit.
        '''
        target_links = set()
        raw_html = link_html
        bs_struct = BeautifulSoup(raw_html, "html.parser")
        for potential_link in bs_struct.find_all('a', href=True):
            link_href = potential_link['href']
            if self.root_url not in link_href:
                link_href = urlparse.urljoin(self.root_url, link_href)
            if (link_href not in self.crawled_links_set) and self.should_visit(link_href) and link_href not in self.emails:
                target_links.add(link_href)
                self.crawled_links_set.add(link_href)
        return target_links

    def should_visit(self, link):
        '''
        Returns true if we're going to visit the link.
        '''
        return not (self.is_media_link(link) or self.is_text_link(link) or self.is_email_link(link))

    def is_media_link(self, link):
        return self.has_extension(self.media_extensions, link)

    def is_text_link(self, link):
        return self.has_extension(self.text_extensions, link)

    def is_email_link(self, link):
        return ("@" in link)

    def has_extension(self, taboo_list, link):
        resource = link.replace(self.root_url, "")
        for taboo in taboo_list:
            if taboo in resource:
                return True
        return False

    #################
    ###### Exit #####
    #################
    def output_professors(self):
        #output the list of
        professor_list = []
        for professor_email in self.emails:
            p = professor.Professor(None, professor_email, self.university_id, None)
            professor_list.append(p)
        return professor_list










