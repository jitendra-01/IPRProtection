// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract PatentRegistry {
    struct Patent {
        string title;
        string abstractData;
        string metadata;
        string contentHash; 
        string ipfsHash;
        address owner;
        uint256 timestamp;
        bool exists;
    }

    mapping(string => Patent) private patents;  
    mapping(address => string[]) private ownerPatents; // Patents owned by an address
    string[] private allContentHashes; // Store all content hashes for retrieval

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
        allContentHashes.push(_contentHash); // Track all patents

        emit PatentRegistered(msg.sender, _contentHash, _ipfsHash, block.timestamp);
    }

    function getPatentsByOwner(address _owner) 
        public 
        view 
        returns (
            string[] memory titles,
            string[] memory abstracts,
            string[] memory metadataList,
            string[] memory contentHashes,
            string[] memory ipfsHashes,
            uint256[] memory timestamps
        ) 
    {
        uint256 count = ownerPatents[_owner].length;
        titles = new string[](count);
        abstracts = new string[](count);
        metadataList = new string[](count);
        contentHashes = new string[](count);
        ipfsHashes = new string[](count);
        timestamps = new uint256[](count);

        for (uint256 i = 0; i < count; i++) {
            string memory contentHash = ownerPatents[_owner][i];
            Patent memory p = patents[contentHash];

            titles[i] = p.title;
            abstracts[i] = p.abstractData;
            metadataList[i] = p.metadata;
            contentHashes[i] = p.contentHash;
            ipfsHashes[i] = p.ipfsHash;
            timestamps[i] = p.timestamp;
        }

        return (titles, abstracts, metadataList, contentHashes, ipfsHashes, timestamps);
    }

    function getAllPatents() 
        public 
        view 
        returns (
            string[] memory titles,
            string[] memory abstracts,
            string[] memory metadataList,
            string[] memory contentHashes,
            string[] memory ipfsHashes,
            address[] memory owners,
            uint256[] memory timestamps
        ) 
    {
        uint256 count = allContentHashes.length;
        titles = new string[](count);
        abstracts = new string[](count);
        metadataList = new string[](count);
        contentHashes = new string[](count);
        ipfsHashes = new string[](count);
        owners = new address[](count);
        timestamps = new uint256[](count);

        for (uint256 i = 0; i < count; i++) {
            string memory contentHash = allContentHashes[i];
            Patent memory p = patents[contentHash];

            titles[i] = p.title;
            abstracts[i] = p.abstractData;
            metadataList[i] = p.metadata;
            contentHashes[i] = p.contentHash;
            ipfsHashes[i] = p.ipfsHash;
            owners[i] = p.owner;
            timestamps[i] = p.timestamp;
        }

        return (titles, abstracts, metadataList, contentHashes, ipfsHashes, owners, timestamps);
    }
}
