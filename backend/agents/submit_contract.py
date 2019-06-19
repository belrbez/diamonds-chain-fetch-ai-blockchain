import time

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address


def call(name: str)-> SmartContract:
    # Create keypair for the contract owner
    provider1 = Entity()
    address1 = Address(provider1)

    # Setting API up
    api = LedgerApi('185.91.52.11', 1002)

    # Need funds to deploy contract
    api.sync(api.tokens.wealth(provider1, 59000000))

    with open(name, "r") as fb: source = fb.read()

    # Create contract
    contract = SmartContract(source)

    # Deploy contract
    api.sync(api.contracts.create(provider1, contract, 2456766))

    print("Wait for txs to be mined ...")
    time.sleep(5)

    # Printing balance of the creating address1
    print(contract.query(api, 'getAccountRides', "1"))

def main():
    call("./full_contract.etch")

if __name__ == '__main__': 
    # Loading contract
    # if len(sys.argv) != 2:
    #   print("Usage: ", sys.argv[0], "[filename]")
    #   exit(-1)
    #
    # with open(sys.argv[1], "r") as fb:
    #   source = fb.read()

    call("./full_contract.etch")