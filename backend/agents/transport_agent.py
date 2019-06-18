#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#   Copyright 2018 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
import pickle
import json
import pprint
import time
from typing import List

from oef.query import Query, Constraint, Eq
from oef.agents import OEFAgent
from oef.messages import CFP_TYPES
from oef.schema import Description
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address

from trip_schema import FROM_LONGITUDE, FROM_LATITUDE


class TransportAgent(OEFAgent):
    """Class that implements the behaviour of the transport agent."""

    transport_description = Description(
        {
            "price_per_km": 10,
            "state": "WAIT",
            "driver_id": "",
            "passengers_ids": ""
        }
    )

    def __init__(self, *args, **kwargs):
      super(TransportAgent, self).__init__(*args, **kwargs)

      self._entity = Entity()
      self._address = Address(self._entity)


    def search(self):

        return

    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: Transport: No trips found. Waiting for next loop...".format(self.public_key))
            time.sleep(3)
            return

        print("[{0}]: Transport: Trips found: {1}".format(self.public_key, agents))
        for agent in agents:
            print("[{0}]: Transport: Sending cfp to trip {1}".format(self.public_key, agent))
            # we send a 'None' query, meaning "give me all the resources you can propose."
            query = None

            price = 1

            # prepare the proposal with a given price.
            proposal = Description({"price_per_km": price})
            print("[{}]: Transport: Sending propose at price: {}".format(self.public_key, price))
            self.send_propose(1, 0, agent, 0, [proposal])
        # self.send_cfp(1, 0, agent, 0, query)
        # self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])


    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Transport: Received accept from {1}.".format(self.public_key, origin))

        # TRIP IN PROGRESS
        print("[{0}]: Transport: Trip in progress.".format(self.public_key))
        time.sleep(5)
        print("[{0}]: Transport: Trip finished.".format(self.public_key))

        # Preparing contract
        # PLACE HOLDER TO PREPARE AND SIGN TRANSACTION
        # decentralized_trip_contract
        contract = {"contract": "data"}

        # Sending contract
        encoded_data = json.dumps(contract).encode("utf-8")
        print("[{0}]: Transport: Sending contract to {1}".format(self.public_key, origin))
        self.send_message(0, dialogue_id, origin, encoded_data)


if __name__ == "__main__":
    agent = TransportAgent("transprt", oef_addr="185.91.52.11", oef_port=10000)
    agent.connect()
    agent.register_service(77, agent.transport_description)


    time.sleep(10)
    query = Query([Constraint(FROM_LONGITUDE.name, Eq(1)), Constraint(FROM_LATITUDE.name, Eq(1))])
    agent.search_services(0, query)

    print("[{}]: Transport: Waiting for trips...".format(agent.public_key))
    try:
        agent.run()
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
