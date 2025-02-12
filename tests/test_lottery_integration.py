from brownie import network
import pytest
from scripts.helpul_scripts import LOCAL_BLOCKCHAIN_ENVIROMENTS, get_account, fund_with_link, get_contract
from scripts.deploy_lottery import deploy_lottery
import time

from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

def test_can_pick_winner():
    #arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    time.sleep(170)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    
