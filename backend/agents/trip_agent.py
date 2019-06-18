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
from email._header_value_parser import Address
from xml.dom.minidom import Entity

from oef.agents import OEFAgent

from typing import List

from oef.messages import CFP_TYPES
from oef.proxy import PROPOSE_TYPES
from oef.query import Eq, Constraint
from oef.query import Query
from oef.schema import Description, Location

import asyncio
import time

from trip_schema import TRIP_DATAMODEL


class TripAgent(OEFAgent):
    def __init__(self, data, *args, **kwargs):
        super(TripAgent, self).__init__(*args, **kwargs)

        self._entity = Entity()
        self._address = Address(self._entity)

        self.data = {
            "account_id": data['account_id'],
            "trip_id": data['trip_id'],
            "from_location": data['from_location'],
            "to_location": data['to_location']
        }
        self.trip_description = Description(self.data, TRIP_DATAMODEL())
        self.possible_trips = []

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, answer with an Accept."""
        print("[{0}]: Trip: Received propose from agent {1}".format(self.public_key, origin))
        for i, p in enumerate(proposals):
            print("[{0}]: Trip: Proposal {1}: {2}".format(self.public_key, i, p.values))
            # if p.values["price_per_km"] <
        print("[{0}]: Trip: Accepting Propose.".format(self.public_key))
        self.send_accept(msg_id, dialogue_id, origin, msg_id + 1)

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        """Extract and print data from incoming (simple) messages."""

        # PLACE HOLDER TO SIGN AND SUBMIT TRANSACTION
        transaction = json.loads(content.decode("utf-8"))
        print("[{0}]: Trip: Received contract from {1}".format(self.public_key, origin))
        print("Trip: READY TO SUBMIT: ", transaction)

        self.stop()



if __name__ == "__main__":
    # create and connect the agent
    agent = TripAgent("TripAgent", oef_addr="185.91.52.11", oef_port=10000)
    agent.connect()
    agent.register_service(77, agent.trip_description)

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
