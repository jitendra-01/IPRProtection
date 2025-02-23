import hashlib
import fitz  
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .services.blockchain import upload_to_blockchain, upload_to_ipfs
from .services.similarity_check import similarity_checker


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
    
    # file_path = pdf_file.temporary_file_path()
    # print(file_path)
    if not title or not keyword or not pdf_file:
            return Response({"message": "Missing fields"})

    # Generate Metadata (comma-separated keywords)
    metadata = ", ".join(keywords)

    # Extract text from PDF
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    pdf_text = " ".join([page.get_text() for page in doc])
    reports = similarity_checker(pdf_text,title)
    # Compute SHA-256 Hash
    content_hash = hashlib.sha256(pdf_text.encode()).hexdigest()

    # Upload PDF to IPFS
    pdf_file.seek(0)
    try:
        ipfs_hash = upload_to_ipfs(files)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    # # # Upload data to blockchain
    try:
        txn_hash = upload_to_blockchain(title, abstract, metadata, content_hash, ipfs_hash)
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
        "report":reports
    }, status=201)
