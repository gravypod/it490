from datetime import datetime
from typing import Union, Optional, Tuple

from app import config, queue
from app.database import Database
from app.models import PlayerCreation, Login, VillainTemplate
from app.models.weather import Weather

server = queue.QueueServer(config.QUEUE_URL, config.QUEUE_TOPIC_APP)
db = Database(config.DATABASE_URL)
weather_scraper_client = queue.QueueClient(config.QUEUE_URL, config.QUEUE_TOPIC_WEATHER)
weather_scraper_client.start()

@server.route('Player.create')
def player_create(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    print('Within handler')
    player_creation = PlayerCreation(
        username=payload['username'],
        password=payload['password'],
        location_name=payload['locationName']
    )
    player = db.player_creation_insert(player_creation)
    return 200, player.to_dict()


@server.route('Player.login')
def player_login(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    login = Login(
        username=payload['username'],
        password=payload['password']
    )

    db.player_login(login)
    return 200, db.player_load(login.username).to_dict()


@server.route('VillainTemplate.create')
def villain_template_create(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    villain_template = VillainTemplate(
        name=payload['name'],
        face_image_url=payload['faceImageUrl']
    )
    villain_template = db.villain_template_create(villain_template)
    return 200, villain_template.to_dict()


@server.route('Player.get')
def player_get(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    player = db.player_load(
        username=payload['username'] if 'username' in payload else None,
        player_id=payload['playerId'] if 'playerId' in payload else None
    )
    return 200, player.to_dict()


@server.route('Weather.get')
def weather_get(payload: dict, metadata: dict) -> Optional[Tuple[int, Union[dict, list]]]:
    location_name = payload['locationName']
    on = datetime.utcnow()

    weather = db.weather_get(location_name, on)

    if weather is None:
        response, status_code = weather_scraper_client.send('Weather.get', {
            'locationName': location_name
        })

        if status_code == 200:
            weather = db.weather_set(Weather(
                id=None,
                location=location_name,
                temperature=response['temperature'],
                phrase=response['phrase'],
                on=on
            ))
        else:
            return status_code, response

    if weather is None:
        return 500, {'message': 'Failed to fetch weather from cache'}

    return 200, weather.to_dict()


server.start()
