from web3 import Web3
import json
import requests

GANACHE_URL="https://eth-sepolia.g.alchemy.com/v2/7K8Kf7K5s0UwJv8sJiHy2-AwegVewk1s"
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

CONTRACT_ADDRESS = "0xf0FFd05090d4a8d0f4581A72d61206d868d0Af22"
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


def upload_to_ipfs(files):
    """Uploads PDF to IPFS using a public IPFS node (Pinata, Infura, or local node)."""
    ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"  # Replace if using another provider
    headers = {
        "pinata_api_key": "e51e86f57ba01788c14e",
        "pinata_secret_api_key": "aaf3d7e2804eec7d7dabb1822473695f20b77541651003ed9d48c409d31dae94",
    }
  
    # print(files)
    response = requests.request("POST", ipfs_url, headers=headers, files=files)

    print(response.json())

    if response.status_code == 200:
        return response.json()["IpfsHash"]
    else:
        raise Exception("Failed to upload to IPFS")

def upload_to_blockchain(title, abstract, metadata, content_hash, ipfs_hash):
    
    """Uploads patent data to the Ethereum blockchain."""
    # const accounts = await window.ethereum.request({ method: "eth_requestAccounts" });
    # const userAddress = accounts[0]; 
    nonce =web3.eth.get_transaction_count(WALLET_ADDRESS)

    gas_estimate =contract.functions.registerPatent(
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
