from web3 import Web3
import json
import requests

GANACHE_URL="https://eth-sepolia.g.alchemy.com/v2/7K8Kf7K5s0UwJv8sJiHy2-AwegVewk1s"
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# CONTRACT_ADDRESS = "0xf0FFd05090d4a8d0f4581A72d61206d868d0Af22"
# CONTRACT_ABI = [
#     {
#       "anonymous": False,
#       "inputs": [
#         {
#           "indexed": True,
#           "internalType": "address",
#           "name": "owner",
#           "type": "address"
#         },
#         {
#           "indexed": False,
#           "internalType": "string",
#           "name": "contentHash",
#           "type": "string"
#         },
#         {
#           "indexed": False,
#           "internalType": "string",
#           "name": "ipfsHash",
#           "type": "string"
#         },
#         {
#           "indexed": False,
#           "internalType": "uint256",
#           "name": "timestamp",
#           "type": "uint256"
#         }
#       ],
#       "name": "PatentRegistered",
#       "type": "event"
#     },
#     {
#       "inputs": [],
#       "name": "getAllPatents",
#       "outputs": [
#         {
#           "internalType": "string[]",
#           "name": "titles",
#           "type": "string[]"
#         },
#         {
#           "internalType": "string[]",
#           "name": "abstracts",
#           "type": "string[]"
#         },
#         {
#           "internalType": "string[]",
#           "name": "metadataList",
#           "type": "string[]"
#         },
#         {
#           "internalType": "string[]",
#           "name": "contentHashes",
#           "type": "string[]"
#         },
#         {
#           "internalType": "string[]",
#           "name": "ipfsHashes",
#           "type": "string[]"
#         },
#         {
#           "internalType": "address[]",
#           "name": "owners",
#           "type": "address[]"
#         },
#         {
#           "internalType": "uint256[]",
#           "name": "timestamps",
#           "type": "uint256[]"
#         }
#       ],
#       "stateMutability": "view",
#       "type": "function"
#     },
#     {
#       "inputs": [
#         {
#           "internalType": "address",
#           "name": "_owner",
#           "type": "address"
#         }
#       ],
#       "name": "getPatentsByOwner",
#       "outputs": [
#         {
#           "internalType": "string[]",
#           "name": "titles",
#           "type": "string[]"
#         },
#         {
#           "internalType": "string[]",
#           "name": "abstracts",
#           "type": "string[]"
#         },
#         {
#           "internalType": "string[]",
#           "name": "metadataList",
#           "type": "string[]"
#         },
#         {
#           "internalType": "string[]",
#           "name": "contentHashes",
#           "type": "string[]"
#         },
#         {
#           "internalType": "string[]",
#           "name": "ipfsHashes",
#           "type": "string[]"
#         },
#         {
#           "internalType": "uint256[]",
#           "name": "timestamps",
#           "type": "uint256[]"
#         }
#       ],
#       "stateMutability": "view",
#       "type": "function"
#     },
#     {
#       "inputs": [
#         {
#           "internalType": "string",
#           "name": "_title",
#           "type": "string"
#         },
#         {
#           "internalType": "string",
#           "name": "_abstractData",
#           "type": "string"
#         },
#         {
#           "internalType": "string",
#           "name": "_metadata",
#           "type": "string"
#         },
#         {
#           "internalType": "string",
#           "name": "_contentHash",
#           "type": "string"
#         },
#         {
#           "internalType": "string",
#           "name": "_ipfsHash",
#           "type": "string"
#         }
#       ],
#       "name": "registerPatent",
#       "outputs": [],
#       "stateMutability": "nonpayable",
#       "type": "function"
#     }
#   ]

CONTRACT_ADDRESS = "0x2E9E4577fc6A8525491010081f28B98de1208B14"
CONTRACT_ABI =   [
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "string",
          "name": "patentId",
          "type": "string"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "oldOwner",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "newOwner",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        }
      ],
      "name": "OwnershipTransferred",
      "type": "event"
    },
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
          "name": "patentId",
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


if web3.is_connected():
  print("connected")
else:
  print("failed")
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# WALLET_ADDRESS = "0xaB0b39BA2764291F09B222fF59E8791a461173A0"
# WALLET_PRIVATE_KEY = "587127fc32144295b773de6e100f0952108ab5ba011bed56ed3dcd480b96a26a "

# WALLET_ADDRESS = "0x7a7577FC751Ee24b4540804528ced6BAe0E4b0fE"
WALLET_ADDRESS = "0x7a7577FC751Ee24b4540804528ced6BAe0E4b0fE"
# WALLET_PRIVATE_KEY = "77ed4fb9d47540d71e9b5d8b673f886dc539d90b2febe9da9210f7d4024fc2c7"
WALLET_PRIVATE_KEY = "77ed4fb9d47540d71e9b5d8b673f886dc539d90b2febe9da9210f7d4024fc2c7"


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
    receipt = web3.eth.wait_for_transaction_receipt(txn_hash,timeout=6000,poll_latency=1)
    # logs = contract.events.PatentRegistered().process_receipt(receipt)
    # return logs[0]['args']['patentId']
    return receipt
    
