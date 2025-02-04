from brownie import Lottery, accounts, config, network, interface
from web3 import Web3
import pytest

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account, "gas_limit": 4000000, "gas_price": Web3.to_wei('20', 'gwei')}
    )
    # Escuchar el evento
    tx = lottery.getEntranceFee()
    receipt = tx.events['PriceUpdated']
    print(f"Price: {receipt['price']}")
