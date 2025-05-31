import React, { useState, useEffect } from "react";
import { ethers } from "ethers";
import "./ReviewDashboard.css";

import { Link } from 'react-router-dom';

const CONTRACT_ADDRESS = "0x2E9E4577fc6A8525491010081f28B98de1208B14"
const PatentRegistryABI =   [
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "string",
          "name": "patentId",
          "type": "string"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "oldOwner",
          "type": "address"
        },
        {
          "indexed": true,
          "internalType": "address",
          "name": "newOwner",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "OwnershipTransferred",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": true,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "patentId",
          "type": "string"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "ipfsHash",
          "type": "string"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "PatentRegistered",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "getAllPatents",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "patentId",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "title",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "abstractData",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "metadata",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "contentHash",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "ipfsHash",
              "type": "string"
            },
            {
              "internalType": "address",
              "name": "owner",
              "type": "address"
            },
            {
              "internalType": "uint256",
              "name": "timestamp",
              "type": "uint256"
            },
            {
              "internalType": "bool",
              "name": "exists",
              "type": "bool"
            }
          ],
          "internalType": "struct PatentRegistry.Patent[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_patentId",
          "type": "string"
        }
      ],
      "name": "getOwnershipHistoryWithTimestamps",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "owners",
          "type": "address[]"
        },
        {
          "internalType": "uint256[]",
          "name": "timestamps",
          "type": "uint256[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_patentId",
          "type": "string"
        }
      ],
      "name": "getPatentByPatentId",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "patentId",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "title",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "abstractData",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "metadata",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "contentHash",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "ipfsHash",
              "type": "string"
            },
            {
              "internalType": "address",
              "name": "owner",
              "type": "address"
            },
            {
              "internalType": "uint256",
              "name": "timestamp",
              "type": "uint256"
            },
            {
              "internalType": "bool",
              "name": "exists",
              "type": "bool"
            }
          ],
          "internalType": "struct PatentRegistry.Patent",
          "name": "",
          "type": "tuple"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_contentHash",
          "type": "string"
        }
      ],
      "name": "getPatentIdByHash",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_owner",
          "type": "address"
        }
      ],
      "name": "getPatentsByOwner",
      "outputs": [
        {
          "components": [
            {
              "internalType": "string",
              "name": "patentId",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "title",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "abstractData",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "metadata",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "contentHash",
              "type": "string"
            },
            {
              "internalType": "string",
              "name": "ipfsHash",
              "type": "string"
            },
            {
              "internalType": "address",
              "name": "owner",
              "type": "address"
            },
            {
              "internalType": "uint256",
              "name": "timestamp",
              "type": "uint256"
            },
            {
              "internalType": "bool",
              "name": "exists",
              "type": "bool"
            }
          ],
          "internalType": "struct PatentRegistry.Patent[]",
          "name": "",
          "type": "tuple[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_title",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_abstractData",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_metadata",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_contentHash",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_ipfsHash",
          "type": "string"
        }
      ],
      "name": "registerPatent",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_patentId",
          "type": "string"
        },
        {
          "internalType": "address",
          "name": "_newOwner",
          "type": "address"
        }
      ],
      "name": "transferOwnership",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ]


const ADMIN_ADDRESS="0x7a7577FC751Ee24b4540804528ced6BAe0E4b0fE"

  const ReviewDashboard = () => {
    const [patents, setPatents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [provider, setProvider] = useState(null);
    const [userAddress, setUserAddress] = useState("");
    const [isAdmin, setIsAdmin] = useState(false);
  
    useEffect(() => {
      if (window.ethereum) {
        const ethProvider = new ethers.BrowserProvider(window.ethereum);
        setProvider(ethProvider);
        connectWallet(ethProvider);
      } else {
        console.error("No Ethereum provider found. Please install MetaMask.");
        setLoading(false);
      }
    }, []);
  
    const connectWallet = async (ethProvider) => {
      try {
        const signer = await ethProvider.getSigner();
        const address = await signer.getAddress();
        setUserAddress(address);
  
        if (address.toLowerCase() === ADMIN_ADDRESS.toLowerCase()) {
          setIsAdmin(true);
          fetchAllPatents(ethProvider);
        } else {
          fetchUserPatents(address, ethProvider);
        }
      } catch (error) {
        console.error("Wallet connection failed:", error);
      }
    };
  
    const fetchAllPatents = async (ethProvider) => {
      try {
        const contract = new ethers.Contract(CONTRACT_ADDRESS, PatentRegistryABI, ethProvider);
        // const [titles, abstracts, metadataList, contentHashes, ipfsHashes, owners, timestamps] = await contract.getAllPatents();
  
        // const formattedPatents = titles.map((title, index) => ({
        //   title,
        //   abstractData: abstracts[index].split(".")[0] + "...", // Show only first sentence
        //   metadata: metadataList[index],
        //   contentHash: contentHashes[index],
        //   ipfsHash: ipfsHashes[index],
        //   owner: owners[index],
        //   timestamp: new Date(Number(timestamps[index]) * 1000).toLocaleString(),
        // }));

        const patentsArray = await contract.getAllPatents();

        const formattedPatents = patentsArray.map((patent) => ({
          title: patent.title,
          abstractData: patent.abstractData.split(".")[0] + ".", // First sentence
          metadata: patent.metadata,
          contentHash: patent.contentHash,
          ipfsHash: patent.ipfsHash,
          owner: patent.owner,
          timestamp: new Date(Number(patent.timestamp) * 1000).toLocaleString(),
        }));
  
        setPatents(formattedPatents);
      } catch (error) {
        console.error("Error fetching all patents:", error);
      } finally {
        setLoading(false);
      }
    };
  
    const fetchUserPatents = async (address, ethProvider) => {
      try {
        const contract = new ethers.Contract(CONTRACT_ADDRESS, PatentRegistryABI, ethProvider);
        // const [patent_id, titles, abstracts, metadataList, contentHashes, ipfsHashes, owner, timestamps] = await contract.getPatentsByOwner(address);
  
        // const formattedPatents = titles.map((title, index) => ({
        //   title,
        //   abstractData: abstracts[index].split(".")[0] + ".", // Show only first sentence
        //   metadata: metadataList[index],
        //   contentHash: contentHashes[index],
        //   ipfsHash: ipfsHashes[index],
        //   owner: address,
        //   timestamp: new Date(Number(timestamps[index]) * 1000).toLocaleString(),
        // }));
        const patentsArray = await contract.getPatentsByOwner();

        const formattedPatents = patentsArray.map((patent) => ({
          title: patent.title,
          abstractData: patent.abstractData.split(".")[0] + ".", // First sentence
          metadata: patent.metadata,
          contentHash: patent.contentHash,
          ipfsHash: patent.ipfsHash,
          owner: patent.owner,
          timestamp: new Date(Number(patent.timestamp) * 1000).toLocaleString(),
        }));

        setPatents(formattedPatents);
      } catch (error) {
        console.error("Error fetching user patents:", error);
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <div style={{ padding: "20px", maxWidth: "1200px", margin: "auto", overflowY: "auto",  wordWrap: "break-word", overflowWrap: "break-word"}}>
        <h1>{isAdmin ? "All Registered Patents" : "Your Patents"}</h1>
        <p style={{fontSize:"18px"}}><strong>Connected as:</strong> {userAddress}</p>
        <p style={{fontSize:"18px"}}><strong>Role:</strong> {isAdmin ? "Admin" : "User"}</p>
  
        {loading ? <p>Loading patents...</p> : (
          <ul>
            {patents.length === 0 ? (
              <p style={{fontSize:"18px"}}>No patents found.</p>
            ) : (
              patents.slice(1).map((patent, index) => (
                <li key={index} style={{ borderBottom: "1px solid #ccc", padding: "10px 0" }}>
                  <h3>
                    <a
                      href={`https://dweb.link/ipfs/${patent.ipfsHash}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{ textDecoration: "none", color: "blue", cursor: "pointer" }}
                    >
                      {patent.title}
                    </a>
                  </h3>
                  <p>{patent.abstractData}...</p>
                  <p><strong>Metadata:</strong> {patent.metadata}&nbsp;&nbsp;&nbsp; <strong>Owner:</strong> {isAdmin ? patent.owner : "You"}&nbsp;&nbsp;&nbsp;<strong>Registered On:</strong> {patent.timestamp}</p>
                </li>
              ))
            )}
          </ul>
        )}
        <Link to="/home/patent-form" className="button">Upload document for patent consideration</Link>
      </div>
    );
  };
export default ReviewDashboard;
  