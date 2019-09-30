from itertools import count
from time import sleep
from traceback import print_exc
from typing import Generator

import requests

from imdbscraper.extraction import HtmlExtractor
from imdbscraper.villain import VillainTemplate


class Scraper:
    def urls(self) -> Generator[str, None, None]:
        for page_number in count(start=1, step=1):
            yield f'https://www.imdb.com/list/ls022928819/?sort=list_order,asc&mode=detail&page={page_number}'

    def request_unil_rerived(self, url) -> requests.Response:
        while True:
            print('[REQUESTING]', url)

            try:
                response = requests.get(url, timeout=10)
            except:
                print_exc()
                response = None

            if not response:
                print('\tFailed... retrying in 10 seconds')
                sleep(10)

            return response

    def villain_templates(self) -> Generator[VillainTemplate, None, None]:
        for url in self.urls():
            response = self.request_unil_rerived(url)
            found_at_least_one_villain = False
            for villain_template in HtmlExtractor(response).villains():
                found_at_least_one_villain = True
                yield villain_template

            if not found_at_least_one_villain:
                # No more villains on page, break out.
                break
