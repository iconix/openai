import html2text
import json
import math
import numpy as np
import pandas as pd
import re
import scraper
import utils

def spotify(songids_file, spotify_token, request_rate=0.25, out_file=None, num_processes=1):
    songids_df = pd.read_json(songids_file)

    # get non-empty spotify ids
    songids_df = songids_df.loc[(~songids_df.spotify_id.isna())]
    relevant_spotify_ids = songids_df.spotify_id

    # spotify audio features API can take up to 100 ids at a time
    num_groups = math.ceil(len(relevant_spotify_ids) / 100)
    groups = np.array_split(relevant_spotify_ids, num_groups)

    api_urls = [_construct_spotify_audio_features_url(g) for g in groups]

    headers = utils.create_auth_headers(bearer_token=spotify_token)
    api_s = scraper.APIScraper(request_rate, headers=headers)
    api_results = utils.run_multi_scraper(api_s, api_urls, num_processes)

    songids_df = songids_df.assign(audio_features=lambda x: None)

    features = []
    for res in api_results:
        features.extend(res['audio_features'])

    songids_df.audio_features = features

    if out_file is not None:
        songids_df.to_json(out_file, orient='records')
    else:
        print(songids_df.to_json(orient='records'))

def genius(songids_file, genius_token, request_rate=0.25, out_file=None, num_processes=1):
    songids_df = pd.read_json(songids_file)

    # get genius ids that have a non-empty corresponding spotify id
    songids_df = songids_df.loc[~songids_df.spotify_id.isna()]
    relevant_genius_ids = songids_df.genius_id

    # get genius song urls
    song_api_urls = [_construct_genius_song_api_url(id) for id in relevant_genius_ids]
    headers = utils.create_auth_headers(bearer_token=genius_token)
    api_s = scraper.APIScraper(request_rate, headers=headers)
    api_results = utils.run_multi_scraper(api_s, song_api_urls, num_processes)

    song_urls = [res['response']['song']['url'] if 'response' in res else '' for res in api_results]

    dom_s = scraper.DOMScraper(request_rate)
    dom_results = utils.run_multi_scraper(dom_s, song_urls, num_processes, ['meta[itemprop="page_data"]'], 'content')

    songids_df = songids_df.assign(genres=lambda x:None, desc=lambda x:None)

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True

    genres = []
    descs = []
    regex = r'tag:([^,]+)'
    for content in dom_results:
        if content is None:
            genres.append(None)
            descs.append(None)
            continue

        sections = json.loads(content)['chartbeat']['sections']

        try:
            matches = re.finditer(regex, sections)
            song_genres = [match.group(1) for match in matches]
        except Exception as e:
            print(f'[WARNING] error getting song genres - setting to None')
            print(e)
            song_genres = None

        genres.append(song_genres)

        try:
            desc = h.handle(json.loads(content)['song']['description']['html'])
        except Exception as e:
            print(f'[WARNING] error getting song desc - setting to None')
            print(e)
            desc = None

        descs.append(desc)

    songids_df.genres = genres
    songids_df.desc = descs

    # TODO: desc == '\n\n?\n\n'

    if out_file is not None:
        songids_df.to_json(out_file, orient='records')
    else:
        print(songids_df.to_json(orient='records'))

def _construct_spotify_audio_features_url(ids):
    # maximum: 100 IDs
    return f'https://api.spotify.com/v1/audio-features?ids={",".join(ids)}'

def _construct_genius_song_api_url(id):
    return f'https://api.genius.com/songs/{id}?text_format=plain'

if __name__ == '__main__':
    import fire; fire.Fire()