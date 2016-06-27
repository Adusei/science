#!/usr/bin/env python

from pprint import pprint
from bs4 import BeautifulSoup
import requests
import json

class EnigmaScraper(object):
    '''

    Output the result to "solutions.json"
    '''

    def __init__(self, base_url):
        '''
        '''

        self.base_url = base_url
        self.pages_to_process, self.company_links, self.results = [], [], {}

    def main(self):
        '''
        1. Find all of the pages we need to process
        2. Find all of the companies on all of the pages
        3. Hit all of those URLS parse the tables and dump out json
        '''
        self.process_base_url()
        self.get_all_company_urls()
        self.scrape_all_company_data()

        print '===-results below-==='
        print self.results
        print '===-results above-==='

        with open('_data/results.json', 'w') as outfile:
            json.dump(self.results, outfile)

        pprint(self.results)

    def get_soup_content(self, url=None):
        '''
        This allows us to easily pasd a URL to this function and get in
        a BeautifulSoup data object in return
        '''

        if not url:
            request_url = self.base_url
        else:
            request_url = url

        request_result = requests.get(request_url)

        if request_result.status_code != 200:
            raise Exception(' %s is an invalid URL' % url)

        content = request_result.content
        soup = BeautifulSoup(content)

        return soup

    def process_base_url(self):
        '''
        In this method we iterate through all urls on this page do two things
            1. Find all of the pages to process
            2  Get all of the company urls on this page

        '''

        soup_content = self.get_soup_content()

        for link in soup_content.find_all('a'):
            link_href = link['href']

            if '?page' in link_href:
                self.pages_to_process.append(link_href)
            elif 'companies' in link_href:
                self.company_links.append(link)


    def get_all_company_urls(self):
        for page in self.pages_to_process:
            page_suffix = page.replace('/companies','')
            soup_content = self.get_soup_content(self.base_url + page_suffix)
            for link in soup_content.find_all('a'):
                if 'companies/' in link:
                    self.company_links.append(link)

    def scrape_all_company_data(self):

        for c in self.company_links[:2]:

            print 'fetching c: %s ' % c

            url_suffix = c['href'].replace('/companies','')
            soup_content = self.get_soup_content(self.base_url + url_suffix)
            page_data = self.parse_page(soup_content)
            if page_data:
                self.results[c['href']] = page_data

    def parse_page(self, page_content):
        '''
        '''
        company_dict = {}

        try:
            company_dict['website'] = page_content.find('td', {'id':'website'}).string
        except AttributeError:
            return None

        print '====='
        print company_dict
        print '====='

        return company_dict


if __name__ == "__main__":
    scraper = EnigmaScraper(base_url = 'http://data-interview.enigmalabs.org/companies')
    scraper.main()
