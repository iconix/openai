from datetime import datetime, timedelta
import html2text
import json
from langdetect import detect, DetectorFactory
from multiprocessing import Pool
import pandas as pd
import re
import scraper
import string
import sys
from urllib.parse import quote
import utils

def review(bloglist_file, api_key, request_rate=0.25, out_file=None, num_processes=1):
    '''Scrape reviews (article-like) of the URLs provided using the Mercury Web Parser (https://mercury.postlight.com/web-parser/).
    '''
    bloglist_df = pd.read_json(bloglist_file)
    bloglist_df.columns = ['url']

    parser_urls = [_construct_mercury_parser_url(url) for url in bloglist_df.url]
    headers = utils.create_auth_headers(api_key=api_key)
    s = scraper.APIScraper(request_rate, headers=headers, res_callback=_handle_article_response)
    results = utils.run_multi_scraper(s, parser_urls, num_processes)

    DetectorFactory.seed = 0 # enforce consistent language detection

    # assumption: no next_page_url handling (assuming 1 page)
    updated_results = []
    for i, res in enumerate(results):
        if not res:
            res = {
                'title': None,
                'author': None,
                'date_published': None,
                'dek': None,
                'lead_image_url': None,
                'content': '',
                'next_page_url': None,
                'url': None,
                'domain': None,
                'excerpt': None,
                'word_count': 0,
                'direction': None,
                'total_pages': None,
                'rendered_pages': None
            }

        res['orig_url'] = bloglist_df.loc[i, 'url']

        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        try:
            res['content'] = h.handle(res['content'])
        except Exception as e:
            print(f'[WARNING] html2text content handling threw an exception - setting content to empty')
            res['content'] = ''
        res['word_count'] = len(res['content'].split())
        try:
            res['lang'] = detect(res['content'])
        except Exception as e:
            #print(f'[WARNING] langdetect threw an exception - setting lang to None')
            res['lang'] = None

        updated_results.append(res)

    print('total word count:', sum([res['word_count'] for res in updated_results]))

    updated_results_df = pd.DataFrame.from_records(updated_results)

    if out_file is not None:
        updated_results_df.to_json(out_file, orient='records')
    else:
        print(updated_results_df.to_json(orient='records'))

def extern_song_ids(hypem_songlist_file, spotify_token=None, genius_token=None, request_rate=0.25, out_file=None, num_processes=1):
    songlist_df = pd.read_json(hypem_songlist_file)

    search_queries = []
    for song in songlist_df.itertuples():
        search_queries.append(_get_song_query(song.title, song.artist))

    if spotify_token is not None:
        spotify_search_urls = [_construct_spotify_search_url(query) for query in search_queries]

    if genius_token is not None:
        genius_search_urls = [_construct_genius_search_url(query) for query in search_queries]

    if spotify_token is not None and genius_token is not None:
        # run spotify and genius in parallel
        parallel_params = zip([spotify_search_urls, genius_search_urls], [spotify_token, genius_token])
        pool = Pool(processes=2)

        # TODO: num_processes > 1 == AssertionError: daemonic processes are not allowed to have children
        print(f'Executing Spotify and Genius scrapes in parallel')
        async_results = [pool.apply_async(utils.run_multi_scraper, (scraper.APIScraper(request_rate, headers=utils.create_auth_headers(bearer_token=bearer_token)), urls, num_processes)) \
            for urls, bearer_token in parallel_params]
        pool_results = []
        for res in async_results:
            pool_results.append(res.get()) # `get` is a blocking call

        pool.close()

        spotify_res = pool_results[0]
        genius_res = pool_results[1]
    elif spotify_token is not None:
        headers = utils.create_auth_headers(bearer_token=spotify_token)
        s = scraper.APIScraper(request_rate, headers=headers)
        spotify_res = utils.run_multi_scraper(s, spotify_search_urls, num_processes)
    elif genius_token is not None:
        headers = utils.create_auth_headers(bearer_token=genius_token)
        s = scraper.APIScraper(request_rate, headers=headers)
        genius_res = utils.run_multi_scraper(s, genius_search_urls, num_processes)
    else:
        print(f'[ERROR] At least one token must be provided: spotify_token or genius_token')
        sys.exit()

    if spotify_token is not None:
        spotify_ids = []
        for res in spotify_res:
            if 'tracks' not in res:
                spotify_ids.append(None)
                continue

            track_items = res['tracks']['items']

            if not len(track_items):
                spotify_ids.append(None)
                continue

            # assumption: taking top search result
            spotify_ids.append(track_items[0]['id'])
    else:
        spotify_ids = [None] * len(songlist_df.itemid)

    if genius_token is not None:
        genius_ids = []
        for res in genius_res:
            if 'response' not in res:
                genius_ids.append(None)
                continue

            hits = res['response']['hits']

            if not len(hits):
                genius_ids.append(None)
                continue

            # assumption: taking top search result
            genius_ids.append(hits[0]['result']['id'])
    else:
        genius_ids = [0] * len(songlist_df.itemid)

    result_df = pd.DataFrame({'itemid': songlist_df.itemid, 'spotify_id': spotify_ids, 'genius_id': genius_ids})
    result_df.genius_id = result_df.genius_id.fillna(0).astype(int)

    if out_file is not None:
        result_df.to_json(out_file, orient='records')
    else:
        print(result_df.to_json(orient='records'))

def song_blogs(tm_out_file, request_rate=0.25, out_file=None, num_processes=1):
    tm_df = pd.read_json(tm_out_file)

    item_ids = set()
    for week in tm_df.songs:
        for song in week:
            item_ids.add(song['itemid']) # artist, title, loved_count, posted_count, time, week

    print(f'{len(item_ids)} unique songs provided.')

    item_ids = list(item_ids) # order
    song_blogs_urls = [_construct_song_blogs_url(item_id) for item_id in item_ids]

    s = scraper.APIScraper(request_rate)
    blogs = utils.run_multi_scraper(s, song_blogs_urls, num_processes)

    result_df = pd.DataFrame({'itemid': item_ids, 'blogs': blogs})

    if out_file is not None:
        result_df.to_json(out_file, orient='records')
    else:
        print(result_df.to_json(orient='records'))

def time_machine(api_key, start_date=datetime.now(), end_date=datetime.now()-timedelta(days=14), days_from_start=None, request_rate=0.25, out_file=None, num_processes=1):
    date_format = '%b-%d-%Y' # May-27-2018

    if not isinstance(start_date, datetime):
        start_date = datetime.strptime(start_date, date_format)

    if isinstance(days_from_start, int):
        end_date = start_date - timedelta(days_from_start)
    elif not isinstance(end_date, datetime):
        end_date = datetime.strptime(end_date, date_format)

    print(f'start_date: {start_date.__format__(date_format)}; end_date: {end_date.__format__(date_format)}')

    weeks = []
    curr_date = start_date
    while curr_date > end_date:
        if curr_date == start_date and curr_date.weekday() is not 0:
            delta = curr_date.weekday()
        else:
            delta = 7

        last_monday = curr_date - timedelta(days=delta)

        weeks.append(last_monday.__format__(date_format))

        curr_date = last_monday

    time_machine_urls = [_construct_time_machine_url(wk) for wk in weeks]
    key_param = f'?key={api_key}' if api_key is not None else None
    s = scraper.APIScraper(request_rate, query_params=key_param)
    songs = utils.run_multi_scraper(s, time_machine_urls, num_processes)

    result_df = pd.DataFrame({'popular_week': weeks, 'songs': songs})

    if out_file is not None:
        result_df.to_json(out_file, orient='records')
    else:
        print(result_df.to_json(orient='records'))

def _construct_mercury_parser_url(url):
    return f'https://mercury.postlight.com/parser?url={url}'

def _construct_song_blogs_url(item_id):
    return f'https://api.hypem.com/v2/tracks/{item_id}/blogs'

def _construct_spotify_search_url(query):
    return f'https://api.spotify.com/v1/search?q={quote(query)}&type=track'

def _construct_genius_search_url(query):
    return f'https://api.genius.com/search?q={quote(query)}'

def _construct_time_machine_url(date):
    return f'https://api.hypem.com/v2/set/popularweek_{date}/tracks'

def _get_song_query(title, artist):
    '''removes following from title:
        - feat
        - w (meaning 'with')
        - punctuation
        - everything after (prod. ) parentheticals
        - parentheticals that don't include 'remix' or 'edit' or 'rework'
       removes following from artist:
        - feat
        - w (meaning 'with')
        - dash
    '''

    if title is None:
        title = ''
    if artist is None:
        artist = ''

    # remove everything after 'prod.' from title
    prod_idx = title.lower().find('prod.')
    title = title[0: prod_idx] if prod_idx > -1 else title

    # lowercase title
    title = title.lower()

    # remove parentheticals that don't include 'remix' OR 'edit' OR 'rework'
    title = _remove_matches_without_words(title, r'\([^)]+\)', ['remix', 'edit', 'rework'])

    # remove punctuation from title
    punct_regex = re.compile('[%s]' % re.escape(string.punctuation))
    title = punct_regex.sub('', title)

    # remove 'feat ' from title
    title = title.replace('feat ', '')

    # remove 'w ' from title
    title = title.replace(' w ', ' ')

    # lowercase and remove 'feat ' from artist
    artist = artist.replace('feat ', '')

    # replace '-' with space
    artist = artist.replace('-', ' ')

    # remove 'w ' from title
    artist = artist.replace(' w ', ' ')

    return f'{title} {artist}'

def _handle_article_response(**kwargs):
    if kwargs is None:
        raise ValueError('_handle_article_response needs args (res, url, remaining_count, rrl)')

    res = kwargs.get('res')
    url = kwargs.get('url')
    remaining_count = kwargs.get('remaining_count')
    rrl = kwargs.get('rrl')

    if res.status_code != 200:
        print(f'[WARNING] request to {url} not successful: {res} {res.text}')
        if res.status_code == 401:
            print(f'[WARNING] request token expired or invalid - abandoning scrape')
            return [[] for i in range(remaining_count)]

        if res.status_code == 502:
            try:
                url = res.request.url

                url_param = 'url='
                idx = url.find(url_param) + len(url_param)
                url = url[:idx] + 'https://web.archive.org/web/1000/' + url[idx:]

                request_url = url
                #print(f'[DEBUG:502] make_rate_limited_request: {request_url}; {utils.RequestVerb.GET}; {res.request.headers}')
                res = rrl.make_rate_limited_request(request_url, utils.RequestVerb.GET, headers=res.request.headers)
            except Exception as e:
                print(f'[WARNING:502] Exception thrown - skipping {url}')
                print(e)
                return []

            if res.status_code != 200:
                print(f'[WARNING:502] request to {url} not successful: {res} {res.text}')
                if res.status_code == 401:
                    print(f'[WARNING:502] request token expired or invalid - abandoning scrape')
                    return [[] for i in range(remaining_count)]
            else:
                try:
                    return res.json()
                except Exception as e:
                    print(f'[WARNING:502] Exception thrown on res.json() for {url}; {res.text} - skipping')
                    return []

        parsed_res = []
    else:
        try:
            parsed_res = res.json()
        except Exception as e:
            print(f'[WARNING] Exception thrown on res.json() for {url}; {res.text} - skipping')
            parsed_res = []

    return parsed_res

def _remove_matches_without_words(target_str, regex, words):
    ''' e.g., TODO: doctest
        target_str = Bad Things feat. Killer Mike (of Run The Jewels) (Official Remix) (Jumanji edition)
        regex = r"\([^)]+\)"
        words = ['remix', 'edit', 'rework']
        output => Bad Things feat. Killer Mike  (Official Remix)
    '''
    target_list = ''.join((c if c.isalpha() else ' ') for c in target_str.lower()).split()

    idx = []
    for word in words:
        if word in target_list:
            idx.append(target_str.find(word))

    for m in re.finditer(regex, target_str, re.MULTILINE | re.IGNORECASE):
        remove = True
        for i in idx:
            if (i > m.start() and i < m.end()):
                remove = False
        if remove:
            target_str = target_str.replace(m.group(), '')

    return target_str

if __name__ == '__main__':
    import fire; fire.Fire()
