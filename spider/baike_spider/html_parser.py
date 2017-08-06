#!/usr/bin/env python
# coding=utf-8
import re

from bs4 import BeautifulSoup


class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        links = soup.find_all('a', href=re.compile(r"/view/"))

    def _get_new_data(self, self1, page_url, soup):
        pass

    def parse(self, page_url, html_count):
        if page_url is None or html_count is None:
            return

        soup = BeautifulSoup(html_count, 'html.parse', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
