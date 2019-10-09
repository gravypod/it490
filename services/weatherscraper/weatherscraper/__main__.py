from typing import Union, Optional, Tuple

from weatherscraper import config, queue
import requests
from bs4 import BeautifulSoup

server = queue.QueueServer(config.QUEUE_URL, config.QUEUE_TOPIC_WEATHER)


@server.route('Weather.get')
def weather_get(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    location_name = payload['locationName']
    response = requests.get(f'https://weather.com/weather/today/l/{location_name}')

    if not response:
        raise queue.ResponseException('Failed to communicate with weather.com')

    dom = BeautifulSoup(response.content, 'html.parser')
    phrase = dom.find('div', {'class': 'today_nowcard-phrase'}).get_text()
    temperature = dom.find('div', {'class': 'today_nowcard-temp'}).get_text()

    data = {
        'phrase': phrase,
        'temperature': float(temperature.replace('°', '').strip())
    }

    print('Weather downloaded:', data)
    return 200, data


server.start()
