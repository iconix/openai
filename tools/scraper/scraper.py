from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from enum import Enum, auto
import html2text
import json
from multiprocessing import Pool
import pandas as pd
import sys
import time
from urllib.parse import urlparse
import utils

USAGE_HELP = 'Run `python scrape.py -- --help` for usage.'

class Scraper(ABC):
    '''All scrapers should implement a `run` method
    '''
    @abstractmethod
    def __init__(self, request_rate):
        self.request_rate = request_rate

    @abstractmethod
    def run(self):
        pass

class APIScraper(Scraper):
    '''Get JSON content returned by an API
    '''
    def __init__(self, request_rate, request_verb=utils.RequestVerb.GET, query_params=None, headers=None, res_callback=utils.handle_json_response):
        self.request_rate = request_rate
        self.request_verb = request_verb
        self.query_params = query_params
        self.headers = headers
        self.res_callback = res_callback

    def run(self, content_urls):
        responses = []
        total = len(content_urls)
        count = 0

        start = time.time()
        for url in content_urls:
            rrl = utils.RequestRateLimiterFactory(self.request_rate)()
            if count is 0:
                print(f'[WARNING] rate_limited _call_api(): max_per_Second:{self.request_rate}')

            try:
                request_url = f'{url}{self.query_params}' if self.query_params is not None else url
                res = rrl.make_rate_limited_request(request_url, self.request_verb, headers=self.headers)
                parsed_res = self.res_callback(res=res, url=url, remaining_count=total-count, rrl=rrl)
            except Exception as e:
                # TODO: could provide 'skip' vs 'abandon' option for exceptions
                print(f'[WARNING] Exception thrown - skipping {url}')
                print(e)
                parsed_res = []

            count += 1
            responses.append(parsed_res)
            utils.print_progress(count, total, urlparse(url).hostname)

        end = time.time()
        print(f'{sum([len(res) for res in responses])} items scraped from {count} urls in {end-start:.2f}s.')

        return responses

class DOMScraper(Scraper):
    '''Scrape content from the DOM of the URLs provided.
    '''
    def __init__(self, request_rate):
        super().__init__(request_rate)

    def run(self, content_urls, content_selectors, select_prop='text'):
        return self._scrape_dom(content_urls, content_selectors, select_prop)

    def _scrape_dom(self, content_urls, content_selectors, select_prop):
        content = []
        total = len(content_urls)
        count = 0

        for url in content_urls:
            soup = utils.Soup.url_to_soup(url, self.request_rate, limit_warning=(count==0))

            count += 1
            utils.print_progress(count, total, urlparse(url).hostname)
            if soup is None:
                print(f'[WARNING] No content found for {url}')
                content.append(None)
            else:
                content.append(utils.Soup.soup_to_content(url, soup, content_selectors, select_prop))

        return content

class IndexScraper(Scraper):
    '''Scrape URLs from the site index using selectors.
    '''
    def __init__(self, request_rate):
        super().__init__(request_rate)

    def run(self, configs):
        #print(configs)

        num_processes = len(configs) # num processes == num configs
        pool = Pool(processes=num_processes)

        print(f'Executing index scrape across max {num_processes} processes')
        async_results = [pool.apply_async(self._scrape_index, (index_url, href_selector, pagination_options)) for index_url, href_selector, pagination_options in configs]
        pool_results = [res.get() for res in async_results] # `get` is a blocking call
        pool.close()

        return pool_results

    def _scrape_index(self, index_url, href_selector, pagination_options):
        if not pagination_options:
            index_urls = [index_url]
        else:
            index_urls = self._parse_pagination_options(index_url, pagination_options)

        content_urls = []
        total = len(index_urls)
        count = 0

        for i_url in index_urls:
            soup = utils.Soup.url_to_soup(i_url, self.request_rate)
            if soup is None:
                print(f'[WARNING] No content urls found for {i_url}')
            else:
                content_urls.extend(utils.Soup.soup_to_index(i_url, soup, href_selector))

            count += 1
            utils.print_progress(count, total, urlparse(i_url).hostname)

        return content_urls

    def _parse_pagination_options(self, index_url, options):
        if options['type'] == 'query_param':
            first_page = options['first_page'] if 'first_page' in options else 1
            return [f'{index_url}{options["query_param"]}{i}' for i in range(first_page, options['last_page']+1)]
        elif options['type'] == 'selector':
            num_pages = options['num_pages'] if 'num_pages' in options else -1
            soup = utils.Soup.url_to_soup(index_url, self.request_rate)
            index_urls = utils.Soup.soup_to_index(index_url, soup, options['href_selector'])
            return index_urls[:num_pages] if num_pages > -1 else index_urls
        else:
            print(f'[WARNING] Required pagination type {options["type"]} is not valid/implemented. Skipping pagination...')
            return [index_url]

class ContentScrapeMethod(Enum):
    '''Allow user to select a content scraping method.
    '''
    DOM = auto()
    RecipeAPI = auto()

class Pipeline(object):
    '''Initialize pipeline for scraping web content.
    Scrape happens in two steps:
        1) content_url scrape
        2) content scrape
    (You can run any of these steps independently using command line args)
    '''

    def __init__(self, config_file=None, scrape_method=None, request_rate=0.25, out_file=None):
        self.config_file = config_file
        self.request_rate = request_rate
        self.scrape_index = IndexScraper(self.request_rate)

        if out_file is not None and not out_file.endswith('.json'):
            print(f'[ERROR] \'{out_file}\' is invalid for JSON output. out_file should end in \'.json\'')
            sys.exit()

        self.out_file = out_file

        if scrape_method is not None:
            try:
                self.scrape_method = ContentScrapeMethod[scrape_method]
            except KeyError as e:
                print(f'[ERROR] {scrape_method} is not a valid ContentScrapeMethod')
                print(e)
                sys.exit()
        else:
            self.scrape_method = ContentScrapeMethod.RecipeAPI

        if self.scrape_method is ContentScrapeMethod.DOM:
            self.scrape_content = DOMScraper(self.request_rate)
        elif self.scrape_method is ContentScrapeMethod.RecipeAPI:
            self.scrape_content = APIScraper(self.request_rate, request_verb=utils.RequestVerb.POST, res_callback=self._handle_augmentation_response)
        else:
            print(f'[ERROR] \'self.scrape_method\' not set or invalid ({self.scrape_method})')
            sys.exit()

        print(f'Initialized Pipeline. config_file: {self.config_file}. scrape_method: {self.scrape_method}.')

    def run(self):
        config_df = self._config_file_to_df()
        config_df = self._scrape_index(config_df)
        config_df = self._scrape_content_async(config_df)

        if self.out_file is None:
            print(config_df)
        else:
            self._config_df_to_file(config_df)

    def _config_file_to_df(self):
        try:
            with open(self.config_file) as f:
                config_df = pd.read_json(f)
                print(f'{len(config_df.index)} sites found in {self.config_file}.')
                if self.out_file is not None:
                    # get columns from original config_file for file output later
                    self.original_columns = list(config_df.columns)
        except TypeError as e:
            print(f'[ERROR] No config file provided to IndexScraper. {USAGE_HELP}')
            print(e)
            sys.exit()

        return config_df

    def _config_df_to_file(self, config_df):
        if self.out_file is not None:
            file_rows = []

            for row in config_df.itertuples(index=True):
                scraped_vals = zip(row.content_urls, row.content)
                for content_url, content in scraped_vals:
                    # TODO: do we want all original_columns in the output? thinking it could be good for debugging failed scrapes...
                    # e.g., maybe 'content_selectors' only output if DOM scrape happened
                    new_row = tuple([content_url, content] + [getattr(row, column) for column in self.original_columns])
                    file_rows.append(new_row)

            file_df = pd.DataFrame.from_records(file_rows, columns=['content_url', 'content'] + self.original_columns)
            file_df.to_json(self.out_file, orient='records')

            print(f'Scrape results saved to {self.out_file}')

    def _construct_augmentation_url(self, url):
        return f'https://www.onenote.com/onaugmentation/clipperextract/v1.0/?renderMethod=extractAggressive&url={url}&lang=en-US'

    def _handle_augmentation_response(self, **kwargs):
        if kwargs is None:
            raise ValueError('_handle_augmentation_response needs args (res, url)')

        res = kwargs.get('res')
        url = kwargs.get('url')

        if res.status_code is not 200:
            print(f'[WARNING] request to {url} not successful: {res}')
            return None

        response_text = res.text

        response_json = json.loads(response_text)[0] # always a list of 1 object
        content_model = response_json['ContentModel']
        if content_model is not 0: # 0 is None
            html = response_json['ContentInHtml']
            html = self._strip_api_metadata(html)
            h = html2text.HTML2Text()
            h.ignore_links = True
            content = h.handle(html)

            if content_model is not 4: # 4 is Recipe
                print(f'[WARNING] {url} content extracted using non-recipe model ({content_model})')
        else:
            content = None

        return content

    def _strip_api_metadata(self, html):
        soup = BeautifulSoup(html, "html.parser")

        for metadata in soup.select('.Metadata'):
            metadata.decompose()

        for thumbnail in soup.select('.Thumbnail'):
            thumbnail.decompose()

        for header in soup.select('.IngredientsContainer h2'):
            header.decompose()

        for header in soup.select('.InstructionsContainer h2'):
            header.decompose()

        return str(soup)

    def _scrape_index(self, config_df):
        start = time.time()

        index_scrape_configs = list(zip(config_df.index_url, config_df.href_selector, config_df.pagination))
        config_df = config_df.assign(content_urls=lambda x:None)
        config_df.content_urls = self.scrape_index.run(index_scrape_configs)

        end = time.time()
        print(f'{sum([len(row) for row in config_df.content_urls])} content urls scraped in {end-start:.2f}s.')

        return config_df

    def _scrape_content_async(self, config_df):
        # TODO: Pool can't handle KeyboardInterrupt on Windows... https://stackoverflow.com/a/35134329 :(

        start = time.time()
        num_processes = len(config_df.index) # num processes == num unique site indices == num rows
        pool = Pool(processes=num_processes)

        print(f'Executing content scrape across max {num_processes} processes')
        async_results = [pool.apply_async(self._scrape_content_by_row, (row,)) for i, row in config_df.iterrows()]
        pool_results = [res.get() for res in async_results] # `get` is a blocking call
        pool.close()

        config_df = pd.DataFrame.from_records(pool_results)

        end = time.time()
        # only counting content that is not None
        print(f'{sum([sum(1 for _ in filter(None.__ne__, row)) for row in config_df.content])} pieces of content scraped in {end-start:.2f}s.')

        return config_df

    def _scrape_content_by_row(self, row):
        if self.scrape_method is ContentScrapeMethod.DOM:
            content = self.scrape_content.run(row.content_urls, row.content_selectors)
        elif self.scrape_method is ContentScrapeMethod.RecipeAPI:
            extract_urls = [self._construct_augmentation_url(url) for url in row.content_urls]
            content = self.scrape_content.run(extract_urls)
        else:
            print(f'[ERROR] \'self.scrape_method\' not set or invalid ({self.scrape_method})')
            sys.exit()

        return row.append(pd.Series([content], index=['content']))

if __name__ == '__main__':
    import fire; fire.Fire(Pipeline)
