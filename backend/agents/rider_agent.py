import pickle
import json
import pprint

from scooter_schema import PRICE_PER_KM, JOURNEY_MODEL
from oef.agents import OEFAgent

from typing import List
from oef.proxy import PROPOSE_TYPES
from oef.query import Eq, Constraint
from oef.query import Query

import asyncio
import time


class RiderAgent(OEFAgent):
    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: No agent found. Stopping...".format(self.public_key))
            self.stop()
            return

        print("[{0}]: Agent found: {1}".format(self.public_key, agents))
        for agent in agents:
            print("[{0}]: Sending to agent {1}".format(self.public_key, agent))
            # we send a 'None' query, meaning "give me all the resources you can propose."
            query = None
            self.send_cfp(1, 0, agent, 0, query)

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, answer with an Accept."""
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin))
        for i, p in enumerate(proposals):
            print("[{0}]: Proposal {1}: {2}".format(self.public_key, i, p.values))
        print("[{0}]: Accepting Propose.".format(self.public_key))
        self.send_accept(msg_id, dialogue_id, origin, msg_id + 1)

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        """Extract and print data from incoming (simple) messages."""

        # PLACE HOLDER TO SIGN AND SUBMIT TRANSACTION
        transaction = json.loads(content.decode("utf-8"))
        print("[{0}]: Received contract from {1}".format(self.public_key, origin))
        print("READY TO SUBMIT: ", transaction)

        self.stop()


def add_agent(data):
    # create and connect the agent
    print('Add agent: ' + data)
    agent = RiderAgent("RiderAgent", oef_addr="185.91.52.11", oef_port=10000)
    agent.connect()

    time.sleep(2)

    query = Query([Constraint(PRICE_PER_KM.name, Eq(True))],
                  JOURNEY_MODEL)

    agent.search_services(0, query)

    time.sleep(1)
    try:
        agent.run()
        time.sleep(3)
    except Exception as ex:
        print("EXCEPTION:", ex)
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
