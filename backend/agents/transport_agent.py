import pickle
import json
import pprint

from random import randint

from agents.trip_schema import JOURNEY_MODEL
from oef.agents import OEFAgent
from oef.messages import CFP_TYPES
from oef.schema import Description
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address


class TransportAgent(OEFAgent):
    """Class that implements the behaviour of the scooter agent."""

    scooter_description = Description(
        {
            "price_per_km": True,
        },
        JOURNEY_MODEL
    )

    def __init__(self, data, *args, **kwargs):
        super(TransportAgent, self).__init__(*args, **kwargs)
        self.data = data
        self._entity = Entity()
        self._address = Address(self._entity)

    #      with open("./full_contract.etch", "r") as fb:
    #          self._source = fb.read()

    #      self.prepare_contract()

    def prepare_contract(self):
        # Setting API up
        self._api = LedgerApi('185.91.52.11', 10002)

        # Need funds to deploy contract
        self._api.sync(self._api.tokens.wealth(self._entity, 5000000))

        # Create contract
        self._contract = SmartContract(self._source)

        # Deploy contract
        self._api.sync(self._api.contracts.create(self._entity, self._contract, 2456766))

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))

        price = 1

        # prepare the proposal with a given price.
        proposal = Description({"price_per_km": price})
        print("[{}]: Sending propose at price: {}".format(self.public_key, price))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Received accept from {1}."
              .format(self.public_key, origin))

        # Preparing contract
        # PLACE HOLDER TO PREPARE AND SIGN TRANSACTION
        contract = {"contract": "data"}

        # Sending contract
        encoded_data = json.dumps(contract).encode("utf-8")
        print("[{0}]: Sending contract to {1}".format(self.public_key, origin))
        self.data['status'] = 'RIDES'
        self.send_message(0, dialogue_id, origin, encoded_data)


def add_transport_agent(data):
    agent = TransportAgent(data, randint(1, 1e9), oef_addr="185.91.52.11", oef_port=10000)
    agent.connect()
    agent.register_service(77, agent.scooter_description)

    print("[{}]: Waiting for clients...".format(agent.public_key))
    try:
        agent.run()
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
