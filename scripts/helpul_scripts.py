from brownie import network, config, accounts, Contract, MockV3Aggregator, VRFCoordinatorMock, LinkToken, interface
from web3 import Web3
from brownie.network.gas.strategies import LinearScalingStrategy

DECIMALS = 8
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]

contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
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

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account, "gas_price": gas_strategy})
    #link_token_contracts =interface.LinkTokenInterface(link_token.address)
    #tx = link_token_contracts.transfer(contract_address, amount, {"from": account, "gas_price": gas_strategy})
    tx.wait(1)
    print("contract funded")
    return tx

def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account, "gas_price": gas_strategy})
    link_token =LinkToken.deploy({"from": account, "gas_price": gas_strategy})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account, "gas_price": gas_strategy})
    print("Mocks deployed")