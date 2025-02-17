import hashlib
import fitz  
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .services.blockchain import upload_to_blockchain, upload_to_ipfs
import re

@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload_patent(request):
    """Handles patent upload, processing, and blockchain registration."""
    
    title = request.data.get("title")
    # abstract = request.data.get("abstract")
    keyword = request.data.get("keywords")  
    pdf_file = request.FILES.get("pdf")
    keywords = keyword.split(",")
    # print(keywords[1])
    if not title or not keyword or not pdf_file:
            return Response({"message": "Missing fields"})

    # Generate Metadata (comma-separated keywords)
    metadata = ", ".join(keywords)

    # Extract text from PDF
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_text = " ".join([page.get_text() for page in doc])

    # extract abstract
    abstract_pattern = r"(?i)abstract\s*[:\n]?\s*(.*?)(?=\n|$)"
    match = re.search(abstract_pattern, pdf_text)
    abstract = match.group(1).strip()
    print(abstract)
    
    # Compute SHA-256 Hash
    content_hash = hashlib.sha256(pdf_text.encode()).hexdigest()

    # Upload PDF to IPFS
    # try:
    #     ipfs_hash = upload_to_ipfs(pdf_file)
    # except Exception as e:
    #     return Response({"error": str(e)}, status=500)
    ipfs_hash ="QmYwAPJzv5CZsnAzt8auVTLKk1CswDczq3Zh1G5kCkjJpX"

    # Upload data to blockchain
    try:
        txn_hash = upload_to_blockchain(title, abstract, metadata, content_hash, ipfs_hash)
    except Exception as e:
        return Response({"error": "Blockchain transaction failed", "details": str(e)}, status=500)

    return Response({
        "message": "Patent successfully uploaded",
        "blockchain_tx": txn_hash,
        "ipfs_hash": ipfs_hash
    }, status=201)
