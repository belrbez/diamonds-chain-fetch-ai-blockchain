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

from oef.agents import OEFAgent

from typing import List

from oef.messages import CFP_TYPES
from oef.proxy import PROPOSE_TYPES
from oef.query import Eq, Constraint
from oef.query import Query
from oef.schema import Description, Location

import asyncio
import time

class TripAgent(OEFAgent):
    trip_description = Description(
        {
            "account_id": "1",
            "trip_id": "1",
            "from_location": 1,
            "to_location": Location(52.2057092, 0.1183431)
        }
    )
    possible_trips = []

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
