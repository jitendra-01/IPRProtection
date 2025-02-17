// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract PatentRegistry {
    struct Patent {
        string title;
        string abstractData;
        string metadata;
        string contentHash;  // SHA-256 hash of the content
        string ipfsHash;     // IPFS CID
        address owner;
        uint256 timestamp;
        bool exists;
    }

    mapping(string => Patent) private patents;  // Mapping from hash to patent data
    mapping(address => string[]) private ownerPatents; // Patents owned by an address

    event PatentRegistered(address indexed owner, string contentHash, string ipfsHash, uint256 timestamp);

    function registerPatent(
        string memory _title,
        string memory _abstractData,
        string memory _metadata,
        string memory _contentHash,
        string memory _ipfsHash
    ) public {
        require(!patents[_contentHash].exists, "Patent already exists!");

        Patent memory newPatent = Patent({
            title: _title,
            abstractData: _abstractData,
            metadata: _metadata,
            contentHash: _contentHash,
            ipfsHash: _ipfsHash,
            owner: msg.sender,
            timestamp: block.timestamp,
            exists: true
        });

        patents[_contentHash] = newPatent;
        ownerPatents[msg.sender].push(_contentHash);

        emit PatentRegistered(msg.sender, _contentHash, _ipfsHash, block.timestamp);
    }

    function getPatent(string memory _contentHash) public view returns (
        string memory title,
        string memory abstractData,
        string memory metadata,
        string memory ipfsHash,
        address owner,
        uint256 timestamp
    ) {
        require(patents[_contentHash].exists, "Patent not found!");

        Patent memory p = patents[_contentHash];
        return (p.title, p.abstractData, p.metadata, p.ipfsHash, p.owner, p.timestamp);
    }

    function getPatentsByOwner(address _owner) public view returns (string[] memory) {
        return ownerPatents[_owner];
    }
}
