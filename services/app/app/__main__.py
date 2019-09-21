from typing import Union, Optional

import pika
from app import config, queue

server = queue.QueueServer(config.QUEUE_URL, config.QUEUE_TOPIC_APP)


@server.route('Player.create')
def player_create(payload: dict, metadata: dict) -> Optional[Union[dict, list]]:
    print('Within handler')
    return {}


server.start()
