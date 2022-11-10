// contracts/MyNFT.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

// For more details on the imported contract: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    // tokenCounter keeps track of all tokenId's. When deploying the contract it starts at 0.
    constructor() public ERC721("Doggie", "DOG") {
        tokenCounter = 0;
    }

    // creating an NFT is just mapping a tokenId to a new address.
    // "_safeMint" gives a token ID to the NFT.
    // The tokenURI or Uniform Resource Identifier on an NFT is a unique identifier of what the token "looks" like.
    // "_setTokenURI" gives the URI code to the token ID.
    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newTokenId;
    }
}
