from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)

# Pass the token URI and account to create collectible transaction.
# The website is URL is: OPENSEA_URL + the contract's address + the token counter of this NFT. "-1" For the most recently minted.
def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx_create_colletible = simple_collectible.createCollectible(
        sample_token_uri, {"from": account}
    )
    tx_create_colletible.wait(1)
    number_of_advanced_collectibles = simple_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    print(
        f"You can view your NFT at: {OPENSEA_URL.format(simple_collectible.address,simple_collectible.tokenCounter()-1)}"
    )
    return simple_collectible


def main():
    deploy_and_create()
