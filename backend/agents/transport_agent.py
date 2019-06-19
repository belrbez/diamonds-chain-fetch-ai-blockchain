import json
import time
from random import randint
from typing import List

import asyncio
from threading import Thread
from fetchai.ledger.crypto import Entity, Address
from fetchai.ledger.api import LedgerApi
from oef.agents import OEFAgent
from oef.query import Query, Constraint, Eq, Distance, GtEq, LtEq
from oef.schema import Description, Location

from agents.transport_schema import TRANSPORT_DATAMODEL
from agents.trip_schema import TRIP_DATAMODEL


class TransportAgent(OEFAgent):
    """Class that implements the behaviour of the transport agent."""

    def __init__(self, data, *args, **kwargs):
        super(TransportAgent, self).__init__(*args, **kwargs)

        self._entity = Entity()
        self._address = Address(self._entity)

        self.data = {
            'price_per_km': data['price_per_km'],
            'state': "WAIT",
            'location_latitude': data['location'].latitude,
            'location_longitude': data['location'].longitude
        }
        self.transport_description = Description(self.data, TRANSPORT_DATAMODEL())
        self.distance_allowed_area = 5
        self.velocity = 0.2
        # self.contract = data['rent_contract']

    def search_drivers(self):
        print("[{0}]: Transport: Searching for Passenger trips {1} with allowed distance {2}..."
              .format(self.public_key, self.data['location_latitude'], self.distance_allowed_area))
        query = Query(
            [Constraint(TRIP_DATAMODEL.FROM_LOCATION_LONGITUDE.name,
                        GtEq(self.data['location_longitude'] - self.distance_allowed_area)),
             Constraint(TRIP_DATAMODEL.FROM_LOCATION_LONGITUDE.name,
                        LtEq(self.data['location_longitude'] + self.distance_allowed_area)),
             Constraint(TRIP_DATAMODEL.FROM_LOCATION_LATITUDE.name,
                        GtEq(self.data['location_latitude'] - self.distance_allowed_area)),
             Constraint(TRIP_DATAMODEL.FROM_LOCATION_LATITUDE.name,
                        LtEq(self.data['location_latitude'] + self.distance_allowed_area))
             ])
        self.search_services(randint(1, 1e9), query)

    def on_decline(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        time.sleep(20)
        print('Restart search after declining')
        self.search_drivers()

    def on_dialogue_error(self, answer_id: int, dialogue_id: int, origin: str):
        pass


    def search_passengers(self):
        print("[{0}]: Transport: Searching for Passenger trips {1} with allowed distance {2}...".format(self.public_key,
                                                                                                        self.data[
                                                                                                            'location'].latitude,
                                                                                                        self.distance_allowed_area))
        query = Query([
            # Constraint(TRIP_DATAMODEL.FROM_LOCATION.name, Eq(self.data['location'])),
            # Distance(self.data['location'], self.distance_allowed_area)),
            # Constraint(TRIP_DATAMODEL.TO_LOCATION.name, Eq(self.data['location'])),
            # Distance(self.data['location'], self.distance_allowed_area)),
        ])
        # query = Query([Constraint(TRIP_DATAMODEL.FROM_LOCATION.name, Distance(self.data['location'], self.distance_allowed_area)),
        #                Constraint(TRIP_DATAMODEL.TO_LOCATION.name, Distance(self.data['location'], self.distance_allowed_area))])
        self.search_services(0, query)

    def update_location(self):
        cur_location: Location = self.data['location']
        # cur_location.distance()
        print("[{0}]: Transport: Driving {1}...".format(self.public_key, cur_location))

    def on_search_result(self, search_id: int, agents: List[str]):
        print('On search result')
        if self.data['state'] == 'DRIVE':
            print("[{0}]: Transport: State is driving, no need to search driver...".format(
                self.public_key))
            return

        # """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: Transport: No trips found. Waiting for next loop...".format(self.public_key))
            time.sleep(10)
            self.search_drivers()
            return

        print("[{0}]: Transport: Trips found: {1}".format(self.public_key, agents))
        for agent in agents:
            print("[{0}]: Transport: Sending proposal (without cfp) to trip {1}".format(self.public_key, agent))
            # prepare the proposal with a given price and current location
            proposal = Description({
                "price_per_km": self.data['price_per_km'],
                "location_latitude": self.data['location_latitude'],
                "location_longitude": self.data['location_longitude'],
            })
            print("[{0}]: Transport: Sending propose with location: {1}".format(self.public_key,
                                                                                self.data['location_latitude']))
            msg_id = randint(1, 1e9)
            self.send_propose(msg_id, 0, agent, 0, [proposal])

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        data = json.loads(content.decode('utf-8'))
        if 'type' in data and data['type'] == 'location':
            new_loop = asyncio.new_event_loop()
            print('Transport: get msg from origin {}'.format(origin))
            Thread(target=self.update_transport_location,
                   args=(origin, Location(data['from_location_latitude'], data['from_location_longitude']),
                         Location(data['to_location_latitude'], data['to_location_longitude']), new_loop)).start()

    def update_transport_location(self, origin, source_loc: Location, target_loc: Location, loop):
        asyncio.set_event_loop(loop)
        self.drive_to_point(origin, source_loc, 'Getting to trip')
        self.drive_to_point(origin, target_loc, 'Trip started')

    def drive_to_point(self, origin, target_point: Location, transp_status):
        cur_loc = Location(self.data['location_latitude'], self.data['location_longitude'])
        x_diff = target_point.latitude - cur_loc.latitude
        y_diff = target_point.longitude - cur_loc.longitude

        diff_ratio = abs(y_diff / x_diff)

        x_velocity = self.velocity / (1 + diff_ratio)
        y_velocity = x_velocity * diff_ratio

        x_diff_sign = -1 if x_diff < 0 else 1
        y_diff_sign = -1 if y_diff < 0 else 1

        time.sleep(1)

        while abs(cur_loc.latitude - target_point.latitude) >= abs(x_velocity) and \
                abs(cur_loc.longitude - target_point.longitude) >= abs(y_velocity):
            cur_loc = Location(cur_loc.latitude + x_velocity * x_diff_sign,
                               cur_loc.longitude + y_velocity * y_diff_sign)
            print('Update location of transport to {} {}'.format(cur_loc.latitude, cur_loc.longitude))
            self.send_transp_loc(origin, cur_loc, transp_status)
            time.sleep(1)
        cur_loc = target_point
        self.send_transp_loc(origin, cur_loc, transp_status)
        self.data['location_latitude'] = cur_loc.latitude
        self.data['location_longitude'] = cur_loc.longitude
        if transp_status == 'Getting to trip':
            print("[{0}]: Transport: {1}.".format(self.public_key, 'Picked up account'))
        else:
            print("[{0}]: Transport: {1}.".format(self.public_key, 'Trip finished'))
            self.send_message(randint(1, 1e9), randint(1, 1e9), origin, json.dumps({
                'type': 'finished'
            }).encode('utf-8'))
            self.data['state'] = 'WAIT'
            self.search_drivers()

    def send_transp_loc(self, origin, loc, status):
        msg_id = randint(1, 1e9)
        d_id = randint(1, 1e9)
        self.send_message(msg_id, d_id, origin, json.dumps({
            'location_latitude': loc.latitude,
            'location_longitude': loc.longitude,
            'type': 'location',
            'status': status
        }).encode('utf-8'))

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Transport: Received accept from {1}.".format(self.public_key, origin))

        # TRIP IN PROGRESS
        print("[{0}]: Transport: Trip in progress.".format(self.public_key))
        self.data['state'] = 'DRIVE'

        # Preparing contract
        # PLACE HOLDER TO PREPARE AND SIGN TRANSACTION
        # decentralized_trip_contract
        # Sending contract
        # encoded_data = json.dumps(self.contract).encode("utf-8")
        contract = {'type': 'contract', "contract": "data"}
        encoded_data = json.dumps(contract).encode("utf-8")

        print("[{0}]: Transport: Sending contract to {1}".format(self.public_key, origin))
        self.send_message(0, dialogue_id, origin, encoded_data)
        self.request_agent_location(origin)

    def request_agent_location(self, origin):
        msg_id = randint(1, 1e9)
        dialogue_id = randint(1, 1e9)
        self.send_message(msg_id, dialogue_id, origin, json.dumps({
            'type': 'request'
        }).encode('utf-8'))

    def on_start_trip(self):
        return
        # schedule.every(10).seconds.do(self.search_passengers, ).tag('driving-jobs')
        # schedule.every(1).seconds.do(self.update_location).tag('driving-jobs')

    def on_finish_drive(self):
        time.sleep(20)
        self.data['state'] = 'WAIT'
        # schedule.clear('driving-jobs')
        print("[{0}]: Transport: Trip finished.".format(self.public_key))
        self.search_drivers()

    # def run(self) -> None:
    #     threading.Timer(10.0, self.search_drivers).start()
    #     print("PostTimer")
    #     self._loop.run_until_complete(self.async_run())


def search_cron(loop, agent):
    asyncio.set_event_loop(loop)
    while 1:
        time.sleep(10)
        agent.search_drivers()


def add_transport_agent(data):
    pub_key = str(randint(1, 1e9)).replace('0', 'A').replace('1', 'B')
    agent = TransportAgent(data, pub_key, oef_addr="185.91.52.11", oef_port=10000)
    agent.connect()
    agent.register_service(randint(1, 1e9), agent.transport_description)
    Thread(target=search_cron, args=(asyncio.new_event_loop(), agent)).start()

    print("[{}]: Transport: Searching for Passenger trips...".format(agent.public_key))
    agent.search_drivers()

    print("[{}]: Transport: Launching new transport agent...".format(agent.public_key))

    try:
        agent.run()
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
