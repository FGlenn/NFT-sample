from brownie import (
    accounts,
    network,
    config,
    LinkToken,
    VRFCoordinatorMock,
    Contract,
)
from web3 import Web3
from pathlib import Path
import requests

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache", "mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and
    return that mock contract.
        Args:
            contract_name (string)
        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
    """
    # "contract_type" gives MockV3Aggregator if "contract_name" is "eth_usd_price_feed"     from mapping "contract_to_mock"
    # "contract_type" gives VRFCoordinatorMock if "contract_name" is "vrf_coordinator"      from mapping "contract_to_mock"
    # "contract_type" gives LinkToken if "contract_name" is "link_token"                    from mapping "contract_to_mock"
    # "if len(contract_type)" = MockV3Aggregator.length. If it isn't empty/zero, deploy mocks
    # "contract_type[-1]" is similar as "MockV3Aggregator[-1]"
    #
    # Get the "contract_address" based on the "contract_name" in config.
    # E.g. "config["networks"][network.show_active()][eth_usd_price_feed]" = "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e"
    # Get the "contract_type.abi" based on the "contract_address" and combine data as "contract".
    # E.g. Get the "MockV3Aggregator.abi" based on "0x8A753747A1Fa494EC906cE90E9f37563A8AF630e" gives "contract".
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000

# "MockV3Aggregator" additionaly requires "decimals" and "initial_value" as requirements for deployment.
# "VRFCoordinatorMock" additionaly requires "link_token.address" as requirements for deployment. Which is the "link_token" mock's address.
def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying Mock LinkToken...")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator...")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("All done!")


# 0.1 LINK fee
# "account = account" use the account set in the "def fund_with_link" argument (account=None here)
# "if account" meaning, if it exists. Otherwise use the "get_account()" function
# "link_token = link_token" use the account set in the "def fund_with_link" argument (link_token=None here)
# "if link_token" meaning, if it exists. Otherwise use the "get_contract("link_token")" function
def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx


# Two ways to get an existing contract
#
# 1: get_contract("link_token")
# contract_address = config["networks"][network.show_active()][contract_name]
# contract = Contract.from_abi(
# contract_type._name, contract_address, contract_type.abi
#
# 2: link_token_contract = interface.LinkTokenInterface(link_token.address)
# tx = link_token_contract.transfer(contract_address, amount, {"from": account})


# https://docs.ipfs.io/reference/http/api/#api-v0-add
# {
#   "Bytes": "<int64>",
#   "Hash": "<string>",
#   "Name": "<string>",
#   "Size": "<string>"
# }
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # The file location - file directory= file name
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        # Example uri : ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
