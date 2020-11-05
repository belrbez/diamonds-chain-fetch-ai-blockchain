# DiamondsChain Team

## InstaDrive.io Project

See: https://devpost.com/software/instadrive-io

\#WhiteNightHACK, blockchain and mobility

blockchain
smartcontract
decentralized
python
FetchAI
angular
mesh
bigchaindb
hashstax

## Inspiration
Each day lots of us make commutes. Let's make it efficient with instadrive.io - shared economy platform for bringing humans and vehicles together.

## What it does
Enables cheaper commutes and more efficient use of rental vehicles. Cars and people (passengers and drivers) are searching for the best option to drive. Also to be more effective, person can take a lift from other person who already drives somewhere and their ways cross each other. Also a person who is a passenger in a joined trip can become a driver after the previous one and continue ride to the destination point. Smart algorithms of choosing the car for a person and for choosing the passenger and driver for a car, make our system effictient and vehicle sharing becomes really sharing as in real life.

Thus this system solves problems: For vehicle sharing providers: makes idle time of cars close to zero. For person: makes rides cheaper and faster For governments: decreases traffic jams For environment: decreases air pollution and fuel combustion

## How we built it
We have the prototype of our solution with Fetch.AI using Python libs, custom components, external integration with Mesh, BigChainDB and other technologies.

The cars are implemented as Autonomous Economic Agents that always are searching for the most effective ride requests. Rides requests are also created as agents for effective searching of cars (including such parameters of search as crossing of trip points). There are two types of people: drivers and passengers. In each ride person can choose if he wants drive or not.

## Challenges we ran into
New technology, that we have been learning as we go with project implementation.

## Accomplishments that we're proud of
Th prototype works on the base of Fetch.AI platform!

## How to build & run backend

* Install Fetch AI dependencies using [documentation](https://fetchai.github.io/oef-sdk-python/oef.html?highlight=send#oef.agents.Agent.send_cfp)
* Run Fetch AI (via docker e.g.)
* Verify Fetch AI OEF SDK Python installed
* `cd backend`
* run `python3 setup.py install`
* run `python3 main.py`


## How to build & run frontend
* `cd carsim-frontend`
* run `npm i`
* run `npm start`
