import hashlib
import fitz  
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .services.blockchain import upload_to_blockchain, upload_to_ipfs
from .services.similarity_check import similarity_checker
from web3 import Web3
from django.core.mail import send_mail

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

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)


def sendmail(to_email, subject, body):
    send_mail(
        subject,
        body,
        'jitendralohani01@gmail.com',  
        [to_email],
        fail_silently=False,
    )

def get_patent_id_by_hash(content_hash):
    try:
        patent_id = contract.functions.getPatentIdByHash(content_hash).call()
        return patent_id
    except Exception as e:
        print(f"Blockchain error: {str(e)}")
        return None


@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_patent(request):
    """Handles patent upload, processing, and blockchain registration."""
    
    title = request.data.get("title")
    keyword = request.data.get("keywords")  
    files = request.FILES
    keywords = keyword.split(",")
    abstract = request.data.get("abstract")
    pdf_file = files.get("file")
    email = request.data.get("email")

    if not title or not keyword or not pdf_file:
            return Response({"message": "Missing fields"})

    # Generate Metadata (comma-separated keywords)
    metadata = ", ".join(keywords)

    # Extract text from PDF
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_text = " ".join([page.get_text() for page in doc])
    

    # Compute SHA-256 Hash
    content_hash = hashlib.sha256(pdf_text.encode()).hexdigest()

    # Upload PDF to IPFS
    # pdf_file.seek(0)
    # try:
    #     ipfs_hash = upload_to_ipfs(files)
    # except Exception as e:
    #     return Response({"error": str(e)}, status=500)
    
    # similarity check
    # reports = similarity_checker(pdf_text,title)

    # # # Upload data to blockchain
    try:
        reports = similarity_checker(pdf_text,title)
        # print('x')
        print(reports)

        max_report = max(reports, key=lambda r: r["TF-IDF Cosine Similarity"])
        if max_report["TF-IDF Cosine Similarity"] > 50:
          patent_id = max_report["Patent_id"]
          plag = max_report["TF-IDF Cosine Similarity"]
          print(plag)
          # result = {
          #   "Patent_id": max_report["Patent_id"],
          #   "TF-IDF Cosine Similarity": max_report["TF-IDF Cosine Similarity"]
          # }
          body=f"Following the analysis of your recent patent submission, our system has identified a notable similarity with an existing patent. The comparison indicates a similarity score of {plag} angainst patent with patent_id of {patent_id}, which exceeds our threshold for potential content overlap."
          sendmail(email,"regarding IPR registration",body)
          return Response({
            "message": "Patent not registered due to exceeding plag",
            # "blockchain_tx": txn_hash,
            # "ipfs_hash": ipfs_hash,
            "report":reports
    }, status=201)
        else:
            # result = None

          pdf_file.seek(0)
          try:
              ipfs_hash = upload_to_ipfs(files)
          except Exception as e:
              return Response({"error": str(e)}, status=500)
          txn_hash = upload_to_blockchain(title, abstract, metadata, content_hash, ipfs_hash)
          print(txn_hash)


          patent_idnew=get_patent_id_by_hash(content_hash)
          print(patent_idnew)
          body=f"We are pleased to inform you that your patent submission titled {title} has been successfully received and registered.Your patent id is {patent_idnew}"

          sendmail(email,"regarding IPR registration",body)
    except Exception as e:
        error_message = str(e)
        if "execution reverted" in error_message:
            return Response({
                 "message":"Patent Already exist"
            })
        return Response({"message": str(e)})

    return Response({
        "message": "Patent successfully uploaded",
        "blockchain_tx": txn_hash,
        "ipfs_hash": ipfs_hash,
    }, status=201)



# transfer ownership
@api_view(["POST"])
def transfer_ownership(request):
    try:
        patent_id = request.data.get("patent_id")  
        new_owner = request.data.get("new_owner")

        if not patent_id or not new_owner:
            return Response({"error": "patent_id and new_owner are required."}, status=400)


        # Sender (should be current patent owner)
        sender_address = "0x7a7577FC751Ee24b4540804528ced6BAe0E4b0fE"  
        private_key = "77ed4fb9d47540d71e9b5d8b673f886dc539d90b2febe9da9210f7d4024fc2c7" 


        # Build and sign transaction
        nonce =web3.eth.get_transaction_count(sender_address)
        gas_estimate =contract.functions.transferOwnership(
        patent_id,new_owner
        ).estimate_gas({'from': sender_address})
        txn = contract.functions.transferOwnership(patent_id, new_owner).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'gas': int(gas_estimate * 1.2),
            'gasPrice': web3.eth.gas_price,
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        return Response({
            "message": "Ownership transferred successfully.",
            "transaction_hash": tx_receipt.transactionHash.hex(),
        })

    except Exception as e:
        return Response({"error": str(e)}, status=500)