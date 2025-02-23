from web3 import Web3
import json
import requests

# Connect to local Ganache blockchain
GANACHE_URL = GANACHE_URL="https://eth-sepolia.g.alchemy.com/v2/7K8Kf7K5s0UwJv8sJiHy2-AwegVewk1s"
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Load smart contract
CONTRACT_ADDRESS = "0x59D44a7E6C4E9edCaC030BeC9399e348284cD4db"
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
if web3.is_connected():
  print("connected")
else:
  print("failed")
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Ganache test account (use one from Ganache UI)
WALLET_ADDRESS = "0xaB0b39BA2764291F09B222fF59E8791a461173A0"
WALLET_PRIVATE_KEY= "587127fc32144295b773de6e100f0952108ab5ba011bed56ed3dcd480b96a26a"

def upload_to_ipfs(files):
    """Uploads PDF to IPFS using a public IPFS node (Pinata, Infura, or local node)."""
    ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"  # Replace if using another provider
    headers = {
        "pinata_api_key": "e51e86f57ba01788c14e",  # Replace with your actual key securely
        "pinata_secret_api_key": "aaf3d7e2804eec7d7dabb1822473695f20b77541651003ed9d48c409d31dae94",  # Replace with your actual key securely
    }
    
    # Open PDF file in binary mode
    with open(pdf_file, 'rb') as file:
        files = {"file": file}
        response = requests.post(ipfs_url, files=files, headers=headers)
        
    if response.status_code == 200:
        return response.json()["IpfsHash"]
    else:
        raise Exception(f"Failed to upload to IPFS. Status Code: {response.status_code}, Response: {response.text}")

def upload_to_blockchain(title, abstract, metadata, content_hash, ipfs_hash):
    
    """Uploads patent data to the Ethereum blockchain."""
    
    nonce = web3.eth.get_transaction_count(WALLET_ADDRESS)

    gas_estimate = contract.functions.registerPatent(
      title, abstract, metadata, content_hash, ipfs_hash
    ).estimate_gas({'from': WALLET_ADDRESS})

    txn = contract.functions.registerPatent(
        title, abstract, metadata, content_hash, ipfs_hash
    ).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': nonce, 
        'gas': int(gas_estimate * 1.2), 
        'gasPrice': web3.eth.gas_price,
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=WALLET_PRIVATE_KEY)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(txn_hash,timeout=600,poll_latency=1)
    return receipt.transactionHash.hex()
