from time import sleep

from imdbscraper import config
from imdbscraper.queue import QueueConnection
from imdbscraper.scraper import Scraper

queue = QueueConnection(config.QUEUE_URL, config.QUEUE_TOPIC_APP)
scraper = Scraper()

for villain_template in scraper.villain_templates():
    # Send template into queue
    queue.send('VillainTemplate.create', villain_template.to_dict())

    # Be nice to CPU & web hosts of imdb. Sleep for some time
    sleep(10)
