// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract PatentRegistry {
    struct SimilarityRecord {
        string patentId;
        uint256 score; // similarity score multiplied by 10000
    }

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
        SimilarityRecord[] topSimilarities;
        string accepted;
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
        string memory _ipfsHash,
        string memory _accepted,
        SimilarityRecord[] memory _topSimilarities
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
        newPatent.accepted = _accepted;


        for (uint256 i = 0; i < _topSimilarities.length; i++) {
            newPatent.topSimilarities.push(
                SimilarityRecord({
                    patentId: _topSimilarities[i].patentId,
                    score: _topSimilarities[i].score
                })
            );
        }

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

    function transferOwnership(string memory _patentId, address _newOwner)
        public
        onlyPatentOwner(_patentId)
    {
        require(_newOwner != address(0), "Invalid new owner address");

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

    // function updatePatent(
    //     string memory _patentId,
    //     string memory _title,
    //     string memory _abstractData,
    //     string memory _metadata,
    //     string memory _ipfsHash,
    //     string memory _accepted,
    //     SimilarityRecord[] memory _topSimilarities
    // ) public onlyPatentOwner(_patentId) {

    // require(patents[_patentId].exists, "Patent does not exist");

    // Patent storage patent = patents[_patentId];
    // patent.title = _title;
    // patent.abstractData = _abstractData;
    // patent.metadata = _metadata;
    // patent.ipfsHash = _ipfsHash;
    // patent.accepted = _accepted;

    // // Replace similarities
    // delete patent.topSimilarities;
    // for (uint256 i = 0; i < _topSimilarities.length; i++) {
    //     patent.topSimilarities.push(
    //         SimilarityRecord({
    //             patentId: _topSimilarities[i].patentId,
    //             score: _topSimilarities[i].score
    //         })
    //     );
    // }
    // }

}
