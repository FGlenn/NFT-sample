from brownie import network, AdvancedCollectible
from scripts.helpful_scripts import get_breed, OPENSEA_URL, get_account

from scripts.advanced_collectible.create_metadata import breed_to_image_uri


def main():
    set_tokenURI()


def set_tokenURI():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles = advanced_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_tokenURI_transaction(
                token_id, advanced_collectible, breed_to_image_uri[breed]
            )


def set_tokenURI_transaction(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata button")
