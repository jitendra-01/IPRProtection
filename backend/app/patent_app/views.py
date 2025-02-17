import hashlib
import fitz  # PyMuPDF for PDF processing
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .services.blockchain import upload_to_blockchain, upload_to_ipfs

@api_view(["POST"])
@parser_classes([MultiPartParser])  # Enables file upload handling
def upload_patent(request):
    """Handles patent upload, processing, and blockchain registration."""
    
    title = request.data.get("title")
    abstract = request.data.get("abstract")
    keywords = request.data.getlist("keywords")  # List of keywords
    pdf_file = request.FILES.get("pdf")

    if not all([title, abstract, pdf_file, keywords]):
        return Response({"error": "Missing required fields"}, status=400)

    # Generate Metadata (comma-separated keywords)
    metadata = ", ".join(keywords)

    # Extract text from PDF
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_text = " ".join([page.get_text() for page in doc])

    # Compute SHA-256 Hash
    content_hash = hashlib.sha256(pdf_text.encode()).hexdigest()

    # Upload PDF to IPFS
    try:
        ipfs_hash = upload_to_ipfs(pdf_file)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

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
