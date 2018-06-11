#!/usr/bin/python -u

from bs4 import BeautifulSoup
from enum import Enum, auto
from rate_limited import rate_limited
import requests
from sys import stdout
from urllib.parse import urljoin

def print_progress(count, total, status=''):
    """
    Source: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    if percents is 100.0:
        stdout.write('\n')
    stdout.flush()

class Soup():
    '''Static helper methods for working with BeautifulSoup
    '''
    @staticmethod
    def url_to_soup(url, request_rate, limit_warning=False):
        try:
            rrl = RequestRateLimiterFactory(request_rate)()
            if limit_warning:
                print(f'[WARNING] rate_limited url_to_soup(): max_per_Second:{request_rate}')
            res = rrl.make_rate_limited_request(url)

            if res.status_code is not 200:
                print(f'[WARNING] request to {url} not successful: {res}')
                return None

            page = res.text
        except Exception as e:
            print(f'[WARNING] Failed to fetch {url}')
            print(e)
            return None

        try:
            soup = BeautifulSoup(page, 'lxml')
        except Exception as e:
            print(f'[WARNING] Failed to parse {url}')
            print(e)
            return None

        return soup

    @staticmethod
    def soup_to_index(url, soup, href_selector):
        content_urls = []

        urls = soup.select(href_selector)
        for u in urls:
            # urljoin here ensures we always have an absolute URL:
            # it treats the first URL as the default for all unspecified parts of the second URL;
            # if the second URL is already absolute, it just uses that one
            content_urls.append(urljoin(url, u.attrs['href']))

        if len(content_urls) is 0:
            print(f'[WARNING] No content urls found for {url}')

        return content_urls

    @staticmethod
    def soup_to_content(url, soup, content_selectors):
        content = {}

        for selector in content_selectors:
            select = soup.select(selector)
            if len(select) > 0:
                content[selector] = '\n'.join([s.text for s in select])
            else:
                print(f'[WARNING] Failed to select content with selector {selector} for url {url}')
                content[selector] = None

        return '\n'.join(content.values())

class RequestVerb(Enum):
    GET = auto()
    POST = auto()

def RequestRateLimiterFactory(rate):
    # if needed: https://www.charlesproxy.com/documentation/using-charles/ssl-certificates
    class RequestRateLimiter:
        # `rate` arg: n for n calls per second  (ex. 3 means 3 calls per second)
        # 1/n for n seconds per call (ex. 0.25 means 4 seconds in between calls)
        @rate_limited(rate)
        def make_rate_limited_request(self, url, verb=RequestVerb.GET, data=None, headers=None):
            base_header = {'User-Agent': 'iconix', 'Connection': 'close', 'cache-control': 'no-cache'}
            if headers is not None:
                headers = {**base_header, **headers}
            else:
                headers = base_header

            if verb is RequestVerb.POST:
                return requests.post(url, data=data, headers=headers, allow_redirects=True)
            else:
                return requests.get(url, headers=headers, allow_redirects=True)

    return RequestRateLimiter
