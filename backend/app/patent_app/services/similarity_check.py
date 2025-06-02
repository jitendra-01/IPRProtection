# import hashlib
# import re
# import fitz
# import requests
# from web3 import Web3
# import pdfplumber
# import nltk
# import numpy as np
# import difflib
# import spacy
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from gensim.models import Word2Vec
# from gensim.utils import simple_preprocess
# from nltk.tokenize import sent_tokenize, word_tokenize
# from sentence_transformers import SentenceTransformer

# GANACHE_URL="https://eth-sepolia.g.alchemy.com/v2/7K8Kf7K5s0UwJv8sJiHy2-AwegVewk1s"
# web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

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

CONTRACT_ADDRESS = "0x93f66BC1B9E9abe405519171d045432ca34D95D6"
CONTRACT_ABI = [
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
            },
            {
              "components": [
                {
                  "internalType": "string",
                  "name": "patentId",
                  "type": "string"
                },
                {
                  "internalType": "uint256",
                  "name": "score",
                  "type": "uint256"
                }
              ],
              "internalType": "struct PatentRegistry.SimilarityRecord[]",
              "name": "topSimilarities",
              "type": "tuple[]"
            },
            {
              "internalType": "string",
              "name": "accepted",
              "type": "string"
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
            },
            {
              "components": [
                {
                  "internalType": "string",
                  "name": "patentId",
                  "type": "string"
                },
                {
                  "internalType": "uint256",
                  "name": "score",
                  "type": "uint256"
                }
              ],
              "internalType": "struct PatentRegistry.SimilarityRecord[]",
              "name": "topSimilarities",
              "type": "tuple[]"
            },
            {
              "internalType": "string",
              "name": "accepted",
              "type": "string"
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
            },
            {
              "components": [
                {
                  "internalType": "string",
                  "name": "patentId",
                  "type": "string"
                },
                {
                  "internalType": "uint256",
                  "name": "score",
                  "type": "uint256"
                }
              ],
              "internalType": "struct PatentRegistry.SimilarityRecord[]",
              "name": "topSimilarities",
              "type": "tuple[]"
            },
            {
              "internalType": "string",
              "name": "accepted",
              "type": "string"
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
        },
        {
          "internalType": "string",
          "name": "_accepted",
          "type": "string"
        },
        {
          "components": [
            {
              "internalType": "string",
              "name": "patentId",
              "type": "string"
            },
            {
              "internalType": "uint256",
              "name": "score",
              "type": "uint256"
            }
          ],
          "internalType": "struct PatentRegistry.SimilarityRecord[]",
          "name": "_topSimilarities",
          "type": "tuple[]"
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

# if web3.is_connected():
#   print("connected")
# else:
#   print("failed")
# contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# # Ensure NLTK resources are available
# nltk.download('punkt_tab')
# nlp = spacy.load('en_core_web_sm')

# # remove special characters 
# def remove_special_characters(text):
#     """Removes special characters from the given text, keeping only letters, numbers, and spaces."""
#     return re.sub(r'[^A-Za-z0-9\s]', '', text)

# def preprocess_text(text):
#     doc = nlp(text.lower())  # Convert to lowercase and tokenize
#     stop_words = nlp.Defaults.stop_words 

#     # Lemmatize and remove stopwords
#     cleaned_text = " ".join(
#         token.lemma_ for token in doc if token.is_alpha and token.text not in stop_words
#     )
#     return cleaned_text

# # Function to compute SHA-256 hash
# def compute_hash(text):
#     return hashlib.sha256(text.encode()).hexdigest()

# # Function to compute TF-IDF cosine similarity
# def tfidf_similarity(text1, text2):
#     vectorizer = TfidfVectorizer().fit_transform([text1, text2])
#     vectors = vectorizer.toarray()
#     return cosine_similarity([vectors[0]], [vectors[1]])[0][0]


# def generate_embedding(text1,text2):
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     vec1 = model.encode(text1, convert_to_numpy=True)
#     vec2 = model.encode(text2, convert_to_numpy=True)
#     # print(vec1)
#     # print(vec2)
#     return cosine_similarity([vec1], [vec2])[0][0]

# # Function to generate a similarity report with highlighted sections
# def generate_similarity_report(text1, text2,title1,title2):

#     hash1 = compute_hash(text1)
#     hash2 = compute_hash(text2)

#     exact_match = hash1 == hash2
#     tfidf_sim = tfidf_similarity(text1, text2)
#     # print(tfidf_sim)
#     bert_sim = generate_embedding(text1,text2)
#     # print(bert_sim)

#     report = {
#         "File 1": title1,
#         "File 2": title2,
#         "SHA-256 Hash Match": "Yes" if exact_match else "No",
#         "TF-IDF Cosine Similarity": round(bert_sim*100,2),
#         "Conclusion": "Highly Similar" if tfidf_sim > 0.8 else "Moderate Similarity" if tfidf_sim> 0.5 else "Low Similarity"
#     }

#     return report

# def similarity_checker(file1,patentId): 

#     try:
#         reports = []
#         # Call the smart contract function
#         patents = contract.functions.getAllPatents().call()

#         # Unpack returned data
#         titles, abstracts, metadata_list, content_hashes, ipfs_hashes, owners, timestamps = patents

#         # Construct response with IPFS URLs
#         for i in range(1,len(titles)):
#             ipfs_url= f"https://dweb.link/ipfs/{ipfs_hashes[i]}"
#             try:
#                 response = requests.get(ipfs_url, timeout=1000)  
#                 response.raise_for_status()  # Raise an error if request fails

#                 pdf_document = fitz.open(stream=response.content, filetype="pdf")
#                 file2 = ""
#                 for page in pdf_document:
#                     file2 += page.get_text("text") + "\n"
                
#                 report = generate_similarity_report(preprocess_text(remove_special_characters(file1)), preprocess_text(remove_special_characters(file2)),title,titles[i])
#                 reports.append(report)
#                 print(report)
                
#             except requests.exceptions.RequestException as e:
#                 ipfs_data = f"Error fetching IPFS data: {str(e)}"
#                 print(ipfs_data)
        
#         return reports

#     except Exception as e:
#         print(str(e))

import hashlib
import re
import fitz
import requests
from web3 import Web3
import nltk
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
# import pinecone
from pinecone import Pinecone, ServerlessSpec

GANACHE_URL="https://eth-sepolia.g.alchemy.com/v2/7K8Kf7K5s0UwJv8sJiHy2-AwegVewk1s"
web3 = Web3(Web3.HTTPProvider(GANACHE_URL))

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

# NLTK and Spacy
nltk.download('punkt')
nlp = spacy.load('en_core_web_sm')

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Pinecone
PINECONE_API_KEY = "pcsk_3anwb8_NwWJVhSXTsb7JCzr8yDCcj8sEo4NbGX9X6EHDvy6iYV8nE6pSbdti26yJsYPnTH"  # Replace with your actual Pinecone API key
# PINECONE_ENV = "us-east-1-aws"  
PINECONE_REGION = "us-east-1"        # Replace with your Pinecone environment, e.g. "us-west1-gcp"
PINECONE_CLOUD = "aws"
INDEX_NAME = "patent-similarity"
# pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
pc = Pinecone(api_key=PINECONE_API_KEY)

INDEX_NAME = "patent-similarity"
# Create Pinecone index if it doesn't exist
# if INDEX_NAME not in pinecone.list_indexes():
#     pinecone.create_index(INDEX_NAME, dimension=384)  # 384 for all-MiniLM-L6-v2 embeddings

# index = pinecone.Index(INDEX_NAME)

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud=PINECONE_CLOUD,
            region=PINECONE_REGION
        )
    )

# Connect to the index
index = pc.Index(INDEX_NAME)

# --- Utility functions ---

def remove_special_characters(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

def preprocess_text(text):
    doc = nlp(text.lower())
    stop_words = nlp.Defaults.stop_words
    cleaned_text = " ".join(
        token.lemma_ for token in doc if token.is_alpha and token.text not in stop_words
    )
    return cleaned_text

def compute_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

def tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]

def get_embedding(text):
    return model.encode(text, convert_to_numpy=True)

def generate_similarity_report(text1, text2, patentId):
    hash1 = compute_hash(text1)
    hash2 = compute_hash(text2)

    exact_match = hash1 == hash2
    tfidf_sim = tfidf_similarity(text1, text2)
    # bert_sim = similarity_score

    report = {
        # "File 1": title1,
        # "File 2": title2,
        "Patent_id": patentId,
        "SHA-256 Hash Match": "Yes" if exact_match else "No",
        "TF-IDF Cosine Similarity": round(tfidf_sim * 100, 2),
        # "BERT Cosine Similarity": round(bert_sim * 100, 2),
        # "Conclusion": "Highly Similar" if tfidf_sim > 0.8 else "Moderate" if tfidf_sim > 0.5 else "Low"
    }

    return report

# --- Main similarity checker with Pinecone ---

# def similarity_checker(file1_text, input_title):
#     try:
#         reports = []

#         patents = contract.functions.getAllPatents().call()
#         # Assuming patents is a list of tuples, extract relevant fields correctly
#         # Adjust this part if needed based on how getAllPatents returns data
#         # For example, if patents is a list of dicts or tuples:
#         # Example assumed fields extraction:
#         titles = [p[1] for p in patents]         # title at index 1
#         ipfs_hashes = [p[5] for p in patents]    # ipfsHash at index 5

#         # Fetch existing vectors metadata from Pinecone (optional, for debug)
#         # We'll maintain a set of patent IDs or titles that are indexed
#         existing_ids = set()
#         query_response = index.query(top_k=1000, include_metadata=True)  # get up to 1000 vectors
#         for match in query_response['matches']:
#             existing_ids.add(match['id'])

#         # For each patent, if not already indexed, fetch and index it
#         for i in range(len(titles)):
#             patent_id = titles[i]  # Using title as ID; you can choose another unique ID
#             if patent_id in existing_ids:
#                 continue  # Skip already indexed patents

#             ipfs_url = f"https://dweb.link/ipfs/{ipfs_hashes[i]}"
#             try:
#                 response = requests.get(ipfs_url, timeout=60)
#                 response.raise_for_status()
#                 pdf_document = fitz.open(stream=response.content, filetype="pdf")

#                 text_content = ""
#                 for page in pdf_document:
#                     text_content += page.get_text("text") + "\n"

#                 clean_text = preprocess_text(remove_special_characters(text_content))
#                 embedding = get_embedding(clean_text).tolist()

#                 # Upsert into Pinecone index
#                 index.upsert([(patent_id, embedding, {"title": patent_id})])
#                 print(f"Indexed patent: {patent_id}")

#             except requests.exceptions.RequestException as e:
#                 print(f"Error fetching IPFS data for {patent_id}: {str(e)}")

#         # Now embed the input document and query Pinecone for similarity
#         input_clean = preprocess_text(remove_special_characters(file1_text))
#         input_embedding = get_embedding(input_clean).tolist()

#         # Query Pinecone
#         query_response = index.query(vector=input_embedding, top_k=5, include_metadata=True)

#         # For each matched patent, generate similarity report
#         for match in query_response['matches']:
#             patent_id = match['id']
#             score = match['score']  # cosine similarity score from Pinecone

#             # To generate detailed report, fetch the patent text from IPFS again or cache it
#             # For simplicity, let's fetch once from IPFS here:
#             idx = titles.index(patent_id)
#             ipfs_url = f"https://dweb.link/ipfs/{ipfs_hashes[idx]}"
#             try:
#                 response = requests.get(ipfs_url, timeout=60)
#                 response.raise_for_status()
#                 pdf_document = fitz.open(stream=response.content, filetype="pdf")

#                 patent_text = ""
#                 for page in pdf_document:
#                     patent_text += page.get_text("text") + "\n"

#                 clean_patent_text = preprocess_text(remove_special_characters(patent_text))
#                 report = generate_similarity_report(input_clean, clean_patent_text, input_title, patent_id, score)
#                 print(report)
#                 reports.append(report)
#             except Exception as e:
#                 print(f"Failed to fetch patent text for report generation: {str(e)}")

#         return reports

#     except Exception as e:
#         print(f"Similarity checker error: {str(e)}")
#         return []

def similarity_checker(file1,title): 

    try:
        reports = []
        # Call the smart contract function
        patents = contract.functions.getAllPatents().call()
        # print("a")
        print(len(patents))
        # Unpack returned data
        # titles, abstracts, metadata_list, content_hashes, ipfs_hashes, owners, timestamps = patents
        # print(titles)
        # Construct response with IPFS URLs
        
        # for i in range(0,len(titles)):
        for i in range(0,len(patents)):
            patentId, title1, abstract, metadata, content_hashe, ipfs_hash, owner, timestamp, exists = patents[i]
            print(patentId)
            ipfs_url= f"https://dweb.link/ipfs/{ipfs_hash}"
            try:
                response = requests.get(ipfs_url, timeout=1000)  
                response.raise_for_status()  # Raise an error if request fails

                pdf_document = fitz.open(stream=response.content, filetype="pdf")
                file2 = ""
                for page in pdf_document:
                    file2 += page.get_text("text") + "\n"
                
                
                report = generate_similarity_report(preprocess_text(remove_special_characters(file1)), preprocess_text(remove_special_characters(file2)),patentId)
                reports.append(report)
                print(report)
                
            except requests.exceptions.RequestException as e:
                ipfs_data = f"Error fetching IPFS data: {str(e)}"
                print(ipfs_data)
        
        return reports

    except Exception as e:
        print(str(e))
        