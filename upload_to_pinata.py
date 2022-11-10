import os
from pathlib import Path
import requests

pinata_base_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"
# Change this filepath to a FOR loop if you want to pin everything.
filepath = "././img/pug.png"
filename = filepath.split("/")[-1:][0]
headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}


# Pin an IPFS file to Pinata


def main():
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1:][0]
        response = requests.post(
            pinata_base_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
        # ipfs_hash = response.json()["Hash"]
        # # ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json
        # image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        # print(image_uri)
        # return image_uri
