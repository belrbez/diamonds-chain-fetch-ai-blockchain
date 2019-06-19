import json
from typing import List
from random import randint

from fetchai.ledger.crypto import Entity, Address
from oef.agents import OEFAgent
from oef.query import Query, Constraint, Eq, Distance
from oef.schema import Description, Location
import sched, time
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
            'location': data['location']
        }
        self.transport_description = Description(self.data, TRANSPORT_DATAMODEL())
        self.distance_allowed_area = 20.0

    def search_drivers(self):
        print("[{}]: Transport: Searching for Passenger trips...".format(self.public_key))
        query = Query(
            [Constraint(TRIP_DATAMODEL.FROM_LOCATION.name, Distance(self.data['location'], self.distance_allowed_area)),
             Constraint(TRIP_DATAMODEL.TO_LOCATION.name, Distance(self.data['location'], self.distance_allowed_area)),
             Constraint(TRIP_DATAMODEL.CAN_BE_DRIVER.name, Eq(True))])
        self.search_services(0, query)

    def search_passengers(self):
        print("[{}]: Transport: Searching for Passenger and Drivers trips...".format(self.public_key))
        query = Query(
            [Constraint(TRIP_DATAMODEL.FROM_LOCATION.name, Distance(self.data['location'], self.distance_allowed_area)),
             Constraint(TRIP_DATAMODEL.TO_LOCATION.name, Distance(self.data['location'], self.distance_allowed_area))])
        self.search_services(0, query)

    def update_location(self):
        cur_location: Location = self.data['location']
        # cur_location.distance()
        print("[{0}]: Transport: Driving {1}...".format(self.public_key, cur_location))

    def on_search_result(self, search_id: int, agents: List[str]):
        if self.data['state'] == 'DRIVE':
            return

        # """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: Transport: No trips found. Waiting for next loop...".format(self.public_key))
            return

        print("[{0}]: Transport: Trips found: {1}".format(self.public_key, agents))
        for agent in agents:
            print("[{0}]: Transport: Sending proposal (without cfp) to trip {1}".format(self.public_key, agent))
            # prepare the proposal with a given price and current location
            proposal = Description({
                "price_per_km": self.data['price_per_km'],
                "location": self.data['location'],
            })
            print("[{0}]: Transport: Sending propose with location: {1}".format(self.public_key, self.data['location']))
            self.send_propose(1, 0, agent, 0, [proposal])

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Transport: Received accept from {1}.".format(self.public_key, origin))

        # TRIP IN PROGRESS
        print("[{0}]: Transport: Trip in progress.".format(self.public_key))
        self.data['state'] = 'DRIVE'

        # Preparing contract
        # PLACE HOLDER TO PREPARE AND SIGN TRANSACTION
        # decentralized_trip_contract
        contract = {"contract": "data"}

        # Sending contract
        encoded_data = json.dumps(contract).encode("utf-8")
        print("[{0}]: Transport: Sending contract to {1}".format(self.public_key, origin))
        self.send_message(0, dialogue_id, origin, encoded_data)

    def on_start_trip(self):
        return
        # schedule.every(10).seconds.do(self.search_passengers, ).tag('driving-jobs')
        # schedule.every(1).seconds.do(self.update_location).tag('driving-jobs')

    def on_finish_drive(self):
        time.sleep(20)
        self.data['state'] = 'WAIT'
        # schedule.clear('driving-jobs')
        print("[{0}]: Transport: Trip finished.".format(self.public_key))


def cron(delay, interval, agent):
    time.sleep(delay)
    while 1:
        agent.search_drivers()
        time.sleep(interval)


def add_transport_agent(data):
    pub_key = str(randint(1, 1e9)).replace('0', 'A').replace('1', 'B')
    agent = TransportAgent(data, pub_key, oef_addr="185.91.52.11", oef_port=10000)
    agent.connect()
    agent.register_service(randint(1, 1e9), agent.transport_description)

    print("[{}]: Transport: PreLaunching new transport agent...".format(agent.public_key))
    cron(5, 1, agent)
    print("[{}]: Transport: Launching new transport agent...".format(agent.public_key))

    try:
        agent.run()
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
