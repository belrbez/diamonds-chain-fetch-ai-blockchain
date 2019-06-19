import json
import time
from typing import List
from random import randint
import schedule
from fetchai.ledger.crypto import Entity, Address
from oef.agents import OEFAgent
from oef.query import Query, Constraint, Eq, Distance
from oef.schema import Description

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
            'position': data['position']
        }
        self.transport_description = Description(self.data, TRANSPORT_DATAMODEL())

    def search_drivers(self):
        print("[{}]: Transport: Searching for Passenger trips...".format(self.public_key))
        # TODO: use TRIP_DATAMODEL.DISTANCE_AREA to compare
        query = Query([Constraint(TRIP_DATAMODEL.FROM_LOCATION.name, Distance(self.data['position'], 20.0)),
                       Constraint(TRIP_DATAMODEL.TO_LOCATION.name, Distance(self.data['position'], 30.0)),
                       Constraint(TRIP_DATAMODEL.CAN_BE_DRIVER.name, Eq(True))])
        self.search_services(0, query)

    def search_passengers(self):
        print("[{}]: Transport: Searching for Passenger and Drivers trips...".format(self.public_key))
        query = Query([Constraint(TRIP_DATAMODEL.FROM_LOCATION.name, Distance(self.data['position'], 20.0)),
                       Constraint(TRIP_DATAMODEL.TO_LOCATION.name, Distance(self.data['position'], 30.0))])
        self.search_services(0, query)

    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: Transport: No trips found. Waiting for next loop...".format(self.public_key))
            time.sleep(3)
            return

        print("[{0}]: Transport: Trips found: {1}".format(self.public_key, agents))
        for agent in agents:
            print("[{0}]: Transport: Sending cfp to trip {1}".format(self.public_key, agent))
            # prepare the proposal with a given price.
            proposal = Description({"price_per_km": self.data['price_per_km']})
            print("[{}]: Transport: Sending propose with price: {}".format(self.public_key, self.data['price_per_km']))
            self.send_propose(1, 0, agent, 0, [proposal])

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Transport: Received accept from {1}.".format(self.public_key, origin))

        # TRIP IN PROGRESS
        print("[{0}]: Transport: Trip in progress.".format(self.public_key))
        self.data['state'] = 'DRIVE'
        schedule.every(10).seconds.do(self.search_passangers)
        time.sleep(5)
        self.data['state'] = 'WAIT'
        print("[{0}]: Transport: Trip finished.".format(self.public_key))

        # Preparing contract
        # PLACE HOLDER TO PREPARE AND SIGN TRANSACTION
        # decentralized_trip_contract
        contract = {"contract": "data"}

        # Sending contract
        encoded_data = json.dumps(contract).encode("utf-8")
        print("[{0}]: Transport: Sending contract to {1}".format(self.public_key, origin))
        self.send_message(0, dialogue_id, origin, encoded_data)


def add_transport_agent(data):
    pub_key = str(randint(1, 1e9)).replace('0', 'A').replace('1', 'B')
    agent = TransportAgent(data, pub_key, oef_addr="185.91.52.11", oef_port=10000)
    agent.connect()
    agent.register_service(randint(1, 1e9), agent.transport_description)

    schedule.every(10).seconds.do(agent.search_drivers)
    print("[{}]: Transport: Launching new transport agent...".format(agent.public_key))

    try:
        agent.run()
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
