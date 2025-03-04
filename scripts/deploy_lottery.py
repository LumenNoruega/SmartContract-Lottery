from scripts.helpul_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, config, network
from brownie.network.gas.strategies import LinearScalingStrategy
import time
gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

def deploy_lottery():

    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account, "gas_price": gas_strategy},
        publish_source = config["networks"][network.show_active()].get("verify", False),
    )
    print("Lottery deployed")
    return lottery
def start_lottery():
    account=get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account, "gas_price": gas_strategy})
    starting_tx.wait(1)
    print("Lottery started!!!")

def enter_lottery():
    account =get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx =lottery.enter({"from": account, "value": value, "gas_price": gas_strategy})
    tx.wait(1)
    print("You entered the lottery")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account, "gas_price": gas_strategy})
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()