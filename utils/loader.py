# ============================================
# LOADER.PY - PDF Loading and Text Extraction
# ============================================
# This module handles:
# 1. Loading PDF files
# 2. Extracting text from PDFs
# 3. Splitting text into manageable chunks

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP



def load_pdf(file_path: str):
    """
    Load a PDF file and extract text.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        List of document objects with text content
    """
    try:
        # Load PDF using LangChain's PyPDFLoader
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        print(f"✓ Successfully loaded PDF: {len(documents)} pages")
        return documents
    
    except Exception as e:
        print(f"✗ Error loading PDF: {str(e)}")
        raise


def split_text_into_chunks(documents: list):
    """
    Split extracted text into smaller chunks.
    
    Why split into chunks?
    - Embeddings work better with focused text
    - Retrieval becomes more precise
    - Prevents token limit issues
    
    Args:
        documents: List of loaded documents
        
    Returns:
        List of text chunks
    """
    # Create a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Split all documents into chunks
    chunks = text_splitter.split_documents(documents)
    
    print(f"✓ Text split into {len(chunks)} chunks")
    print(f"  - Average chunk size: {CHUNK_SIZE} characters")
    print(f"  - Overlap: {CHUNK_OVERLAP} characters")
    
    return chunks


def process_pdf(file_path: str):
    """
    Complete pipeline: Load PDF → Split into chunks.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        List of text chunks ready for embedding
    """
    documents = load_pdf(file_path)
    chunks = split_text_into_chunks(documents)
    return chunks
