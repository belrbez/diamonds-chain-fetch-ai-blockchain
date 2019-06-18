import flask
import json
import os
from agents.rider_agent import add_agent
import asyncio

app = flask.Flask(__name__)


def to_json(data):
    return json.dumps(data)


@app.route("/journey", methods=['POST'])
def add_journey_request():
    data = flask.request.json
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    add_agent(data)
    return 'ok'


if __name__ == '__main__':
    app.run(port=os.environ.get('SERVER_PORT', 8001))

