// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

// For more details on the imported contract: https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

// This contract has inherited two contract modules "ERC721" and "VRFConsumerBase".

// The "VRFConsumerBase.sol" contract has a constructor built in which requires two addresses
// The "_vrfCoordinator" is the address which checks if the numbers are random.
// The "_link" address as a payment node for it's services.
// Besides a "keyhash" and a "fee" needs to be determined.
// The "keyhash" address uniquely identifies the Chainlink node that wil be used. Go to: https://docs.chain.link/docs/vrf-contracts/.
// The "fee" is how much oracle fees will be paid to the node.
contract AdvancedCollectible is ERC721, VRFConsumerBase {
    // State variables
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;

    // Enums
    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }
    // Mappings
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;

    // Events
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    // creating an NFT is just mapping a tokenId to a new address.
    // "_safeMint" gives a token ID to the NFT.
    // The tokenURI or Uniform Resource Identifier on an NFT is a unique identifier of what the token "looks" like.
    // "_setTokenURI" gives the URI code to the token ID.
    // STEP 1: SEND REQUEST with "requestRandomness"
    // Sending out a request to the Chainlink oracle to generate a random number
    // Emiting an event in order to see the stored arguments passed in transaction logs.

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    // STEP 2: RETRIEVE DATA with "fulfillRandomness"
    // Retrieving a random number from the Chainlink oracle
    // The random number is being devided by the total amount of players in the list. This leaves a random number: 0<number<total length
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    // https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // pug, shiba inu, st bernard
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner or not approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
