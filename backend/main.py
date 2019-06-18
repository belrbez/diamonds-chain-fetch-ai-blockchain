import flask
import json
import os
from agents.rider_agent import add_agent
import asyncio

app = flask.Flask(__name__)

agents = {}


def to_json(data):
    return json.dumps(data)


@app.route("/journey", methods=['POST'])
def add_journey_request():
    data = flask.request.json
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    add_agent(data)
    agents[data['id']] = data
    return 'ok'


@app.route('/journey/<id>', methods=['GET'])
def get_journey_request(id: str):
    if id not in agents:
        flask.abort(404)
    return to_json(agents[id])


if __name__ == '__main__':
    app.run(port=os.environ.get('SERVER_PORT', 8001))
