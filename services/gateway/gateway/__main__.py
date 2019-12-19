from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from waitress import serve
from gateway import config
from gateway.queue import QueueConnection

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = config.JWT_TOKEN
jwt = JWTManager(app)

rpc = QueueConnection(config.QUEUE_URL, config.QUEUE_TOPIC_APP)


@app.route('/logins', methods=['POST'])
def player_login():
    body, status_code = rpc.send('Player.login', request.json, make_jsonified=False)

    if status_code != 200:
        return jsonify(body), status_code

    access_token = create_access_token(
        identity=body['id'],
        user_claims=body
    )
    return access_token, 200


@app.route('/players', methods=['POST'])
def player_create():
    return rpc.send('Player.create', request.json)


@app.route('/players/<player_id>', methods=['GET'])
def player_get(player_id: str):
    return rpc.send('Player.get', {
        'playerId': int(player_id)
    })


@app.route('/weather/<location_name>')
@jwt_required
def weather_get(location_name: str):
    return rpc.send('Weather.get', {
        'locationName': location_name
    })


@app.route('/protected', methods=['GET'])
@jwt_required
def protected_example():
    return rpc.send('VillainTemplate.create', {
        'name': 'Hello World',
        'faceImageUrl': 'http://example.com/image2.png'
    })


@app.route('/inventories/<inventory_id>')
@jwt_required
def inventory_get(inventory_id: str):
    return rpc.send('Inventory.get', {
        'inventory_id': int(inventory_id)
    })

@app.route('/inventories/<inventory_id>', methods=['PUT'])
@jwt_required
def inventory_put():
    return rpc.send('Inventory.put', request.json)


rpc.start()
serve(app, host='0.0.0.0', port=80)
