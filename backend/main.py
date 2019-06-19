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
    add_trip_agent(data, trips)


@app.route("/trips", methods=['POST'])
def add_journey_request():
    data = flask.request.json
    data['trip_id'] = uuid4().hex
    data['status'] = 'WAIT'
    data['from_location'] = Location(data['start']['longitude'], data['start']['latitude'])
    data['to_location'] = Location(data['end']['longitude'], data['end']['latitude'])
    data['distance_area'] = uniform(0, 2)
    data['position'] = data['from_location']
    Thread(target=add_agent_to_oef, args=(data,)).start()
    return to_json({"trip_id": data['trip_id']})


@app.route('/trips/<trip_id>', methods=['GET'])
def get_journey_request(trip_id: str):
    if trip_id not in trips:
        flask.abort(404)
    data = dict(trips[trip_id])
    data['from_location'] = {
        'longitude': data['from_location_longitude'],
        'latitude': data['from_location_latitude']
    }
    data['to_location'] = {
        'longitude': data['to_location_longitude'],
        'latitude': data['to_location_longitude']
    }
    data['position'] = {
        'longitude': data['position'].longitude,
        'latitude': data['position'].latitude
    }
    print(str(data['position']))
    return to_json(data)


def add_transport_agent_to_oef():
    print('Attempt to add transport agent')
    data = {
        'id': uuid4().hex,
        'location': Location(uniform(59.932097364508536, 59.93209736450854),
                             uniform(30.312159061431885, 30.31215906143189)),
        'price_per_km': uniform(1, 3),
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
