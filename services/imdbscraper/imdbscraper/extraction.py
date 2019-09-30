from typing import Generator

from requests import Response
from bs4 import BeautifulSoup, Tag

from imdbscraper.villain import VillainTemplate


class HtmlExtractor:
    def __init__(self, response: Response):
        self.dom = BeautifulSoup(response.content)

    def villains(self) -> Generator[VillainTemplate, None, None]:
        dom_villain_list: Tag = self.dom.find('div', {
            'class': 'lister-list'
        })
        for dom_villain_list_item in dom_villain_list.find_all('div', {'class': 'lister-item'}):
            dom_villain_list_item: Tag = dom_villain_list_item
            dom_villain_list_item_image: Tag = dom_villain_list_item.find('img')
            dom_villain_list_item_header: Tag = dom_villain_list_item.find('h3', {
                'class': 'lister-item-header'
            }).find('a')
            yield VillainTemplate(
                name=dom_villain_list_item_header.text.strip(),
                face_image_url=dom_villain_list_item_image['src'].strip()
            )
