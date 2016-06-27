#!/usr/bin/env python

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
        self.pages_to_process, self.company_links, self.results = [], [], []
        self.page_indicator = '/companies/?page=' ## how i know an href is a page
        self.company_resource_prefix = '/companies'

    def main(self):
        '''
        1. Find all of the pages we need to process
        2. Find all of the companies on all of the pages
        3. Hit all of those URLS parse the tables and dump out json
        '''

        ## get all of the pages ( there should be ten )
        self.process_base_url()
        assert(len(self.pages_to_process) == 10)

        ## get all of the pages ( there should be 100 )
        self.get_all_company_urls()
        assert(len(self.company_links) == 100)

        ## hit those URLs and get the data ##
        self.scrape_all_company_data()

        ## check to see that the parser worked properly... ##
        assert(len(self.results) == 100)

        ## output the data
        with open('_data/solution.json', 'w') as outfile:
            json.dump(self.results, outfile)


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
        Here we figure out what the pages are that we need to process.

        We find the max paginator and append all possilbe pages to the
        self.pages_to_process list.  We will process the companies on the base
        later when processing all of the pages that we figure out we need
        to process here.
        '''

        page_numbers = []
        soup_content = self.get_soup_content()

        for link in soup_content.find_all('a'):
            href = link['href']

            if self.page_indicator in href:
                page_numbers.append(int(href.replace(self.page_indicator,'')))

        ## find all avaiable pages based on the max pagination
        self.pages_to_process = [self.page_indicator + str(p) for p in\
            xrange(1, max(page_numbers) + 1)]


    def get_all_company_urls(self):
        '''
        Iterate through all the pages in the paginator, and find the
        href tag that will take us to an individual company page.

        How we do this is iterrate through the pages that we need to process
        make sure that we are not adding the paginator links, or the base url

        Finally we append the link to the company link list.  The Main method
        will ensure that we have the correct number of companies that we need
        to provess before we actually scrape the data.
        '''

        for page in self.pages_to_process:

            page_suffix = page.replace(self.company_resource_prefix, '')
            soup_content = self.get_soup_content(self.base_url + page_suffix)
            for link in soup_content.find_all('a'):
                link_href = link['href']
                if link_href == self.company_resource_prefix:
                    continue ## don't add the base url to company links
                elif link_href == self.company_resource_prefix + '/':
                    continue ## some links are /companies some are /companies/
                elif link_href == '#':
                    continue ## dont add these blank links..
                elif self.page_indicator not in link_href:
                    self.company_links.append(link)

    def scrape_all_company_data(self):

        for c in self.company_links:

            url_suffix = c['href'].replace(self.company_resource_prefix, '')
            soup_content = self.get_soup_content(self.base_url + url_suffix)
            page_data = self.parse_page(soup_content)
            if page_data:
                self.results.append({c['href'] : page_data})

    def parse_page(self, page_content):
        '''
        Look up elements by ID.

        If this was a production script, I would get all of the TDs and
        iterate through them, adding the key/values as they appear as opposed
        to looking them up by the ID attribute.

        The perfomrnace however very much depends on the way that BeautifulSoup
        finds these elements and what type of data structure the pages are in.

        I would bet that since there are 9 keys, the page content is being
        iterated over 9 times... but for now, given the small page size this
        approach should be sufficient.

        However, in order to look into this I would have to analyze the
        data structure of "page_content".  Depending on how this data is stored
        and how the "find" method works, this actually could be a pretty fast
        way to get the keys when dealing with larger page sizes.
        '''

        company_dict = {
            'website': page_content.find('td', {'id':'website'}).string,
            'name': page_content.find('td', {'id':'name'}).string,
            'street_address': page_content.find('td', {'id':'street_address'}).string,
            'street_address_2': page_content.find('td', {'id':'street_address_2'}).string,
            'city': page_content.find('td', {'id':'city'}).string,
            'state': page_content.find('td', {'id':'state'}).string,
            'zipcode': page_content.find('td', {'id':'zipcode'}).string,
            'phone_number': page_content.find('td', {'id':'phone_number'}).string,
            'website': page_content.find('td', {'id':'website'}).string,
            'description':page_content.find('td', {'id':'description'}).string,
        }

        return company_dict


if __name__ == "__main__":
    scraper = EnigmaScraper(base_url = 'http://data-interview.enigmalabs.org/companies')
    scraper.main()
