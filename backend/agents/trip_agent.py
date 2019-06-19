import json
from email._header_value_parser import Address
from fetchai.ledger.crypto import Entity, Address

from random import randint
from oef.agents import OEFAgent
from oef.messages import CFP_TYPES
from oef.proxy import PROPOSE_TYPES
from oef.schema import Description, Location

import time
from agents.trip_schema import TRIP_DATAMODEL


class TripAgent(OEFAgent):
    def __init__(self, data, *args, **kwargs):
        super(TripAgent, self).__init__(*args, **kwargs)

        self._entity = Entity()
        self._address = Address(self._entity)

        self.data = {
            "account_id": data['account_id'],
            "can_be_driver": data['can_be_driver'],
            "trip_id": data['trip_id'],
            "from_location_latitude": float(data['from_location'].latitude),
            "from_location_longitude": float(data['from_location'].longitude),
            "to_location_latitude": float(data['to_location'].latitude),
            "to_location_longitude": float(data['to_location'].longitude),
            "distance_area": data['distance_area']
        }
        self.trip_description = Description(self.data, TRIP_DATAMODEL())
        self.possible_trips = []

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, answer with an Accept."""
        print("[{0}]: Trip: Received propose from agent {1}".format(self.public_key, origin))
        # if pos_loc.distance(proposals['location']) > self.data['distance_area']:
        #     print("[{0}]: Trip: Proposal with location rejected {1}: {2}".format(self.public_key, proposals["location"]))
        #     return
        # for i, p in enumerate(proposals):
        #     if p.values['location']:
        # TODO: check if proposals['location'] is near trip
        print("[{0}]: Trip: Accepting Propose.".format(self.public_key))
        self.send_accept(msg_id, dialogue_id, origin, msg_id + 1)

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        """Extract and print data from incoming (simple) messages."""

        # PLACE HOLDER TO SIGN AND SUBMIT TRANSACTION

        print("[{0}]: Trip: Received contract from {1}".format(self.public_key, origin))
        transaction = json.loads(content.decode("utf-8"))
        print("[{0}]: Trip: READY TO SUBMIT transaction: {1}".format(self.public_key, transaction))

        self.stop()


def add_trip_agent(data):
    # create and connect the agent
    pub_key = str(randint(1, 1e9)).replace('0', 'A').replace('1', 'B')
    agent = TripAgent(data, pub_key, oef_addr="127.0.0.1", oef_port=10000)
    agent.connect()
    msg_id = randint(1, 1e9)
    agent.register_service(msg_id, agent.trip_description)
    print('Add agent Trip: ', data['name'], str(agent.trip_description.values.get('from_location_longitude')))

    try:
        print("[{0}]: Trip: request for a trip sent.".format(agent.public_key))
        agent.run()
    except Exception as ex:
        print("EXCEPTION:", ex)
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
