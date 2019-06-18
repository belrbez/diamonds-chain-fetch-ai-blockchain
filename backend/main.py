import asyncio
import json
from os import environ
from random import uniform
from threading import Thread
from uuid import uuid4
from oef.schema import Location

import flask

from agents.transport_agent import add_transport_agent
from agents.trip_agent import add_trip_agent

app = flask.Flask(__name__)

trips = {}


def to_json(data):
    return json.dumps(data)


def add_agent_to_oef(data):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    add_trip_agent(data)


@app.route("/trips", methods=['POST'])
def add_journey_request():
    data = flask.request.json
    data['trip_id'] = uuid4().hex
    data['status'] = 'WAIT'
    data['from_location'] = Location(data['start']['longitude'], data['start']['latitude'])
    data['to_location'] = Location(data['end']['longitude'], data['end']['latitude'])
    data['distance_area'] = uniform(0, 2)
    Thread(target=add_agent_to_oef, args=(data,)).start()
    trips[data['account_id']] = data
    return 'ok'


@app.route('/trips/<trip_id>', methods=['GET'])
def get_journey_request(trip_id: str):
    if trip_id not in trips:
        flask.abort(404)
    return to_json(trips[trip_id])


def add_transport_agent_to_oef():
    print('Attempt to add transport agent')
    data = {
        'id': uuid4().hex,
        'position': Location(uniform(0, 10), uniform(0, 10)),
        'status': 'WAIT'
    }
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print('Appear transport agent: ' + str(data))
    add_transport_agent(data)


if __name__ == '__main__':

    transport_number = environ.get('TRANSPORT_NUMBER', 3)
    for i in range(transport_number):
        Thread(target=add_transport_agent_to_oef).start()

    app.run(port=environ.get('SERVER_PORT', 8001))
