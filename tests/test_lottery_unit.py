from brownie import Lottery, accounts, config, network, interface, exceptions
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.helpul_scripts import LOCAL_BLOCKCHAIN_ENVIROMENTS, get_account, fund_with_link, get_contract
import pytest
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    #arrange
    lottery = deploy_lottery()
    #act
    expected_entrance_fee = Web3.to_wei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    #assert
    assert expected_entrance_fee == entrance_fee

def test_cant_enter_unless_started():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    #act
    lottery = deploy_lottery()
    #assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee(), "gas_price": gas_strategy})

def test_can_start_and_enter_lottery():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account, "gas_price": gas_strategy})
    #act
    lottery.enter({"from": account, "value": lottery.getEntranceFee(), "gas_price": gas_strategy})
    #assert
    assert lottery.players(0) == account

def test_can_end_lottery():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account, "gas_price": gas_strategy})
    lottery.enter({"from": account, "value": lottery.getEntranceFee(), "gas_price": gas_strategy})
    fund_with_link(lottery)
    #act
    lottery.endLottery({"from": account, "gas_price": gas_strategy})
    #assert
    assert lottery.lottery_state() == 2

def test_can_pick_winner():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account, "gas_price": gas_strategy})
    lottery.enter({"from": account, "value": lottery.getEntranceFee(), "gas_price": gas_strategy})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee(), "gas_price": gas_strategy})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee(), "gas_price": gas_strategy})
    fund_with_link(lottery)

    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()

    transaction = lottery.endLottery({"from": account, "gas_price": gas_strategy})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG= 777
    get_contract("vrf_coordinator").callBackWithRandomness(request_id, STATIC_RNG, lottery.address, {"from": account, "gas_price": gas_strategy})
    
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() > starting_balance_of_account



