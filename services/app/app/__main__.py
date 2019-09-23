from typing import Union, Optional, Tuple

from app import config, queue
from app.database import Database
from app.models import PlayerCreation

server = queue.QueueServer(config.QUEUE_URL, config.QUEUE_TOPIC_APP)
db = Database(config.DATABASE_URL)


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


server.start()
