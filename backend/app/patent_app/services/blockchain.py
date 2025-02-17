from web3 import Web3
import json
import requests

# Connect to local Ganache blockchain
GANACHE_URL = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Load smart contract
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Replace with deployed contract address
CONTRACT_ABI = [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "owner",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "contentHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "ipfsHash",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "PatentRegistered",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_contentHash",
          "type": "string"
        }
      ],
      "name": "getPatent",
      "outputs": [
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
          "name": "",
          "type": "string[]"
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
if web3.is_connected():
  print("connected")
else:
  print("failed")
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Ganache test account (use one from Ganache UI)

def upload_to_ipfs(pdf_file):
    """Uploads PDF to IPFS using a public IPFS node (Pinata, Infura, or local node)."""
    ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"  # Replace if using another provider
    headers = {
        "pinata_api_key": "Your_Pinata_API_Key",
        "pinata_secret_api_key": "Your_Pinata_Secret",
    }
    
    files = {"file": pdf_file}
    response = requests.post(ipfs_url, files=files, headers=headers)

    if response.status_code == 200:
        return response.json()["IpfsHash"]
    else:
        raise Exception("Failed to upload to IPFS")

def upload_to_blockchain(title, abstract, metadata, content_hash, ipfs_hash):
    """Uploads patent data to the Ethereum blockchain."""
    
    txn = contract.functions.registerPatent(
        title, abstract, metadata, content_hash, ipfs_hash
    ).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS),
        'gas': 500000,
        'gasPrice': web3.to_wei('10', 'gwei'),
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=WALLET_PRIVATE_KEY)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    return web3.eth.wait_for_transaction_receipt(txn_hash).transactionHash.hex()
