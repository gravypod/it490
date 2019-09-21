from flask import Flask, request
from waitress import serve
from gateway import config
from gateway.queue import QueueConnection

app = Flask(__name__)

rpc = QueueConnection(config.QUEUE_URL, config.QUEUE_TOPIC_APP)


@app.route('/players', methods=['POST'])
def player_create():
    return rpc.send('Player.create', request.json)


rpc.start()
serve(app, host='0.0.0.0', port=80)
