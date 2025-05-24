import hashlib
import re
import fitz
import requests
from web3 import Web3
import pdfplumber
import nltk
import numpy as np
import difflib
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from nltk.tokenize import sent_tokenize, word_tokenize
from sentence_transformers import SentenceTransformer

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

# Ensure NLTK resources are available
nltk.download('punkt_tab')
nlp = spacy.load('en_core_web_sm')

# remove special characters 
def remove_special_characters(text):
    """Removes special characters from the given text, keeping only letters, numbers, and spaces."""
    return re.sub(r'[^A-Za-z0-9\s]', '', text)

def preprocess_text(text):
    doc = nlp(text.lower())  # Convert to lowercase and tokenize
    stop_words = nlp.Defaults.stop_words 

    # Lemmatize and remove stopwords
    cleaned_text = " ".join(
        token.lemma_ for token in doc if token.is_alpha and token.text not in stop_words
    )
    return cleaned_text

# Function to compute SHA-256 hash
def compute_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Function to compute TF-IDF cosine similarity
def tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    return cosine_similarity([vectors[0]], [vectors[1]])[0][0]


def word2vec_similarity(text1, text2):
    sentences = [simple_preprocess(sent) for sent in sent_tokenize(text1) + sent_tokenize(text2)]
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

    def get_avg_vector(text):
        words = simple_preprocess(text)
        vectors = [model.wv[word] for word in words if word in model.wv]
        return np.mean(vectors, axis=0) if vectors else np.zeros(100)

    vec1 = get_avg_vector(text1)
    vec2 = get_avg_vector(text2)

    return cosine_similarity([vec1], [vec2])[0][0]

# def generate_embedding(text):
#     model = SentenceTransformer('all-MiniLM-L6-v2')
#     text1 = remove_special_characters(text)
#     text1 = preprocess_text(text)
#     return model.encode(text, convert_to_numpy=True)

def generate_embedding(text1,text2):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    vec1 = model.encode(text1, convert_to_numpy=True)
    vec2 = model.encode(text2, convert_to_numpy=True)
    # print(vec1)
    # print(vec2)
    return cosine_similarity([vec1], [vec2])[0][0]

# Function to find longest common subsequence (LCS)
def find_lcs(text1, text2):
    seq_matcher = difflib.SequenceMatcher(None, text1, text2)
    match = seq_matcher.find_longest_match(0, len(text1), 0, len(text2))
    return text1[match.a: match.a + match.size]

# Function to highlight similar words using SpaCy
def highlight_similar_words(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    words1 = {token.text.lower() for token in doc1 if token.is_alpha}
    words2 = {token.text.lower() for token in doc2 if token.is_alpha}
    common_words = words1.intersection(words2)

    return common_words

# Function to generate a similarity report with highlighted sections
def generate_similarity_report(text1, text2,title1,title2):

    hash1 = compute_hash(text1)
    hash2 = compute_hash(text2)

    exact_match = hash1 == hash2
    tfidf_sim = tfidf_similarity(text1, text2)
    # print(tfidf_sim)
    word2vec_sim = word2vec_similarity(text1, text2)
    bert_sim = generate_embedding(text1,text2)
    # print(bert_sim)
    common_phrase = find_lcs(text1, text2)
    common_words = highlight_similar_words(text1, text2)

    report = {
        "File 1": title1,
        "File 2": title2,
        "SHA-256 Hash Match": "Yes" if exact_match else "No",
        "TF-IDF Cosine Similarity": round(bert_sim*100,2),
        # "Word2Vec Cosine Similarity": round(word2vec_sim * 100, 2),
        "Longest Common Phrase": common_phrase if len(common_phrase) > 10 else "None",
        "Common Words": list(common_words)[:10],  
        "Conclusion": "Highly Similar" if tfidf_sim > 0.8 else "Moderate Similarity" if tfidf_sim> 0.5 else "Low Similarity"
    }

    return report

def similarity_checker(file1,title): 

    try:
        reports = []
        # Call the smart contract function
        patents = contract.functions.getAllPatents().call()

        # Unpack returned data
        titles, abstracts, metadata_list, content_hashes, ipfs_hashes, owners, timestamps = patents

        # Construct response with IPFS URLs
        
        for i in range(1,len(titles)):
            ipfs_url= f"https://dweb.link/ipfs/{ipfs_hashes[i]}"
            try:
                response = requests.get(ipfs_url, timeout=1000)  
                response.raise_for_status()  # Raise an error if request fails

                pdf_document = fitz.open(stream=response.content, filetype="pdf")
                file2 = ""
                for page in pdf_document:
                    file2 += page.get_text("text") + "\n"
                
                report = generate_similarity_report(preprocess_text(remove_special_characters(file1)), preprocess_text(remove_special_characters(file2)),title,titles[i])
                reports.append(report)
                print(report)
                
            except requests.exceptions.RequestException as e:
                ipfs_data = f"Error fetching IPFS data: {str(e)}"
                print(ipfs_data)
        
        return reports

    except Exception as e:
        print(str(e))
        
