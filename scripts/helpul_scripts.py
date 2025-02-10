from brownie import network, config, accounts, Contract, MockV3Aggregator
from web3 import Web3
from brownie.network.gas.strategies import LinearScalingStrategy

DECIMALS = 8
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
}


gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

def get_account(id=None, index=None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIROMENTS
    ):
        return accounts[0]
    
    return accounts.add(config["wallets"]["from_key"])
    
def get_contract(contract_name):
    """
    toma el address de contrato de brownie-config, si esta definido. 
    en caso contrario despliega mocks de ese contrato

    Args:
        contract_name (string): 
    
    Returns:
        brownie.network.contract.ProjectContract: implementacion mas
        reciente de este contrato
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
    print("Mocks deployed")