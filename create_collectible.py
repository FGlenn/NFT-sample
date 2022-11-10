from brownie import AdvancedCollectible, network, config
from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
)
from web3 import Web3
from scripts.advanced_collectible.create_metadata import create_metadata
from scripts.advanced_collectible.set_tokenuri import set_tokenURI


def main():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creating_tx = advanced_collectible.createCollectible({"from": account})
    print("New token has been created!")
    creating_tx.wait(1)
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    create_metadata()
    set_tokenURI()
