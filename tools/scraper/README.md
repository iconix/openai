## Run

Full pipeline (defaults to `APIScraper`):

    python -u scraper.py run --config_file=config.json --out_file=recipes.json

    python -u scraper.py run --config_file=config.json --scrape_method=DOM

`IndexScraper`:

    python -u scraper.py scrape_index run --configs='[("https://www.epicurious.com/search?content=recipe", ".recipe-content-card a[itemprop=\"url\"]", {"type": "query_param", "query_param": "&page=", "last_page": 2}), ("https://www.allrecipes.com/recipes/17235/everyday-cooking/allrecipes-magazine-recipes/", ".fixed-recipe-card__info > a", {}), ("https://www.foodnetwork.com/recipes/recipes-a-z", ".m-PromoList__a-ListItem > a", {"type": "selector", "href_selector": "a.o-IndexPagination__a-Button", "num_pages": 2}), ("https://cookpad.com/us", ".card.feed__card > a", {}), ("https://www.tasteofhome.com/winning-recipes/grand-prize-winning-recipes/", "a.rd_recipe_group_title", {}), ("https://www.tasteofhome.com/recipes/publication/taste-of-home-magazine-recipes", "a.rd_recipe_group_title", {}), ("https://www.bbcgoodfood.com/search/recipes", ".teaser-item__title > a", {})]'

`APIScraper`:

    python -u scraper.py scrape_content run --content_urls='["https://www.epicurious.com/recipes/food/views/rhubarb-custard-cake"]'

_Note_: No content will be returned from the above example: the AugmentationAPI extractor actually does not work on epicurious.com (without html in the request body)

`DOMScraper`:

    python -u scraper.py scrape_content run  --scrape_method=DOM --content_urls='["https://www.epicurious.com/recipes/food/views/rhubarb-custard-cake"]' --content_selectors='["div[itemprop=\"description\"]", "div[itemprop=\"recipeInstructions\"] .preparation-groups"]'

### Get reviews

Get popular songs from the past on HypeM with `time_machine`:

    python -u reviews.py time_machine <hypem_key> --request_rate=1 --out_file=time_machine_5yrs.json --days_from_start=1825

Get blogs that talked about popular songs on HypeM with `song_blogs`:

    python -u reviews.py song_blogs time_machine_5yrs.json --request_rate=2 --out_file=song_blogs_5yrs.json --num_processes=4

Get Spotify and/or Genius ids for songs with HypeM ids with `extern_song_ids`:

    python -u reviews.py extern_song_ids cleaned_songlist_sample.json --spotify_token=<spotify_token> --genius_token=<genius_token> --request_rate=3 --out_file=songids_sample.json

Get reviews of URLs with `review`:

    python -u reviews.py review bloglist_sample.json <mercury_key> --request_rate=8 --out_file=blog_content_sample.json --num_processes=8

### Get features

Get audio features with `spotify`:
    python -u features.py spotify songids_5yrs.json <spotify_token> --request-rate=1 --out_file=song_features_spotify_5yrs.json

Get song genre and description with `genius`:
    python -u features.py genius song_features_spotify_5yrs.json <genius_token> --request-rate=8 --num_processes=8 --out_file=song_features_5yrs.json
