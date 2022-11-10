from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import network
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time


def test_create_collectible_integration():
    # arange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("This test is only for testing in live blockchain environments.")
    account = get_account()
    # act
    advanced_collectible, creating_tx = deploy_and_create()
    time.sleep(210)
    # assert
    assert advanced_collectible.tokenCounter() == 1
