import React, { useState, useEffect } from "react";
import { ethers } from "ethers";
import "./ReviewDashboard.css";

import { Link } from 'react-router-dom';
const CONTRACT_ADDRESS = "0xf0FFd05090d4a8d0f4581A72d61206d868d0Af22" // Replace with your deployed contract address.
const PatentRegistryABI=[

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
          "name": "contentHash",
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
          "internalType": "string[]",
          "name": "titles",
          "type": "string[]"
        },
        {
          "internalType": "string[]",
          "name": "abstracts",
          "type": "string[]"
        },
        {
          "internalType": "string[]",
          "name": "metadataList",
          "type": "string[]"
        },
        {
          "internalType": "string[]",
          "name": "contentHashes",
          "type": "string[]"
        },
        {
          "internalType": "string[]",
          "name": "ipfsHashes",
          "type": "string[]"
        },
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
          "internalType": "address",
          "name": "_owner",
          "type": "address"
        }
      ],
      "name": "getPatentsByOwner",
      "outputs": [
        {
          "internalType": "string[]",
          "name": "titles",
          "type": "string[]"
        },
        {
          "internalType": "string[]",
          "name": "abstracts",
          "type": "string[]"
        },
        {
          "internalType": "string[]",
          "name": "metadataList",
          "type": "string[]"
        },
        {
          "internalType": "string[]",
          "name": "contentHashes",
          "type": "string[]"
        },
        {
          "internalType": "string[]",
          "name": "ipfsHashes",
          "type": "string[]"
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
        const [titles, abstracts, metadataList, contentHashes, ipfsHashes, owners, timestamps] = await contract.getAllPatents();
  
        const formattedPatents = titles.map((title, index) => ({
          title,
          abstractData: abstracts[index].split(".")[0] + ".", // Show only first sentence
          metadata: metadataList[index],
          contentHash: contentHashes[index],
          ipfsHash: ipfsHashes[index],
          owner: owners[index],
          timestamp: new Date(Number(timestamps[index]) * 1000).toLocaleString(),
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
        const [titles, abstracts, metadataList, contentHashes, ipfsHashes, timestamps] = await contract.getPatentsByOwner(address);
  
        const formattedPatents = titles.map((title, index) => ({
          title,
          abstractData: abstracts[index].split(".")[0] + ".", // Show only first sentence
          metadata: metadataList[index],
          contentHash: contentHashes[index],
          ipfsHash: ipfsHashes[index],
          owner: address,
          timestamp: new Date(Number(timestamps[index]) * 1000).toLocaleString(),
        }));
  
        setPatents(formattedPatents);
      } catch (error) {
        console.error("Error fetching user patents:", error);
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <div style={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
        <h1>{isAdmin ? "All Registered Patents" : "Your Patents"}</h1>
        <p style={{fontSize:"18px"}}><strong>Connected as:</strong> {userAddress}</p>
        <p style={{fontSize:"18px"}}><strong>Role:</strong> {isAdmin ? "Admin" : "User"}</p>
  
        {loading ? <p>Loading patents...</p> : (
          <ul>
            {patents.length === 0 ? (
              <p style={{fontSize:"18px"}}>No patents found.</p>
            ) : (
              patents.map((patent, index) => (
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
                  <p><strong>Abstract:</strong> {patent.abstractData}...</p>
                  <p><strong>Metadata:</strong> {patent.metadata}</p>
                  <p><strong>Owner:</strong> {isAdmin ? patent.owner : "You"}</p>
                  <p><strong>Registered On:</strong> {patent.timestamp}</p>
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
  