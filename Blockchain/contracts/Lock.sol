// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract PatentRegistry {
    struct OwnershipRecord {
        address owner;
        uint256 timestamp;
    }

    struct Patent {
        string patentId;
        string title;
        string abstractData;
        string metadata;
        string contentHash;
        string ipfsHash;
        address owner;
        uint256 timestamp;
        bool exists;
    }

    uint256 private patentCounter = 0;

    mapping(string => Patent) private patents;
    mapping(string => string) private hashToPatentId;
    mapping(address => string[]) private ownerPatents;
    mapping(string => OwnershipRecord[]) private ownershipHistory;


    string[] private allPatentIds;

    event PatentRegistered(address indexed owner, string patentId, string ipfsHash, uint256 timestamp);
    event OwnershipTransferred(string indexed patentId, address indexed oldOwner, address indexed newOwner, uint256 timestamp);

    modifier onlyPatentOwner(string memory _patentId) {
        require(patents[_patentId].exists, "Patent does not exist");
        require(patents[_patentId].owner == msg.sender, "Only the patent owner can perform this action");
        _;
    }

    function generatePatentId() internal returns (string memory) {
        patentCounter += 1;
        return string(abi.encodePacked("IPR-", uint2str(patentCounter)));
    }

    function registerPatent(
        string memory _title,
        string memory _abstractData,
        string memory _metadata,
        string memory _contentHash,
        string memory _ipfsHash
    ) public returns (string memory) {
        string memory newPatentId = generatePatentId();

        Patent storage newPatent = patents[newPatentId];
        newPatent.patentId = newPatentId;
        newPatent.title = _title;
        newPatent.abstractData = _abstractData;
        newPatent.metadata = _metadata;
        newPatent.contentHash = _contentHash;
        newPatent.ipfsHash = _ipfsHash;
        newPatent.owner = msg.sender;
        newPatent.timestamp = block.timestamp;
        newPatent.exists = true;

        hashToPatentId[_contentHash] = newPatentId;
        ownerPatents[msg.sender].push(newPatentId);
        allPatentIds.push(newPatentId);

        ownershipHistory[newPatentId].push(OwnershipRecord({
            owner: msg.sender,
            timestamp: block.timestamp
        }));

        emit PatentRegistered(msg.sender, newPatentId, _ipfsHash, block.timestamp);
        return newPatentId;
    }

    function getPatentIdByHash(string memory _contentHash) public view returns (string memory) {
        return hashToPatentId[_contentHash];
    }


    function transferOwnership(string memory _patentId, address _newOwner)
        public
        onlyPatentOwner(_patentId)
    {
        require(_newOwner != address(0), "Invalid new owner address");
        require(msg.sender == patents[_patentId].owner, "Access denied: Not the current owner");
        address oldOwner = patents[_patentId].owner;
        patents[_patentId].owner = _newOwner;

        string[] storage oldOwnerList = ownerPatents[oldOwner];
        for (uint256 i = 0; i < oldOwnerList.length; i++) {
            if (keccak256(bytes(oldOwnerList[i])) == keccak256(bytes(_patentId))) {
                oldOwnerList[i] = oldOwnerList[oldOwnerList.length - 1];
                oldOwnerList.pop();
                break;
            }
        }

        ownerPatents[_newOwner].push(_patentId);

        ownershipHistory[_patentId].push(OwnershipRecord({
            owner: _newOwner,
            timestamp: block.timestamp
        }));

        emit OwnershipTransferred(_patentId, oldOwner, _newOwner, block.timestamp);
    }

    function getOwnershipHistoryWithTimestamps(string memory _patentId)
        public
        view
        returns (address[] memory owners, uint256[] memory timestamps)
    {
        require(patents[_patentId].exists, "Patent does not exist");
        require(msg.sender == patents[_patentId].owner, "Access denied: Not the current owner");

        uint256 count = ownershipHistory[_patentId].length;
        owners = new address[](count);
        timestamps = new uint256[](count);

        for (uint256 i = 0; i < count; i++) {
            owners[i] = ownershipHistory[_patentId][i].owner;
            timestamps[i] = ownershipHistory[_patentId][i].timestamp;
        }

        return (owners, timestamps);
    }

    function getPatentByPatentId(string memory _patentId)
        public
        view
        returns (Patent memory)
    {
        require(patents[_patentId].exists, "Patent does not exist");
        return patents[_patentId];
    }

    function getAllPatents() public view returns (Patent[] memory) {
        uint256 count = allPatentIds.length;
        Patent[] memory result = new Patent[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = patents[allPatentIds[i]];
        }
        return result;
    }

    function getPatentsByOwner(address _owner) public view returns (Patent[] memory) {
        uint256 count = ownerPatents[_owner].length;
        Patent[] memory result = new Patent[](count);
        for (uint256 i = 0; i < count; i++) {
            string memory pid = ownerPatents[_owner][i];
            result[i] = patents[pid];
        }
        return result;
    }

    function uint2str(uint256 _i) internal pure returns (string memory str) {
        if (_i == 0) return "0";
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        j = _i;
        while (j != 0) {
            bstr[--k] = bytes1(uint8(48 + j % 10));
            j /= 10;
        }
        str = string(bstr);
    }
}
