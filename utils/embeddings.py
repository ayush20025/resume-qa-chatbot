# ============================================
# EMBEDDINGS.PY - Converting Text to Vectors
# ============================================
# This module handles:
# 1. Creating embeddings for text chunks
# 2. Building FAISS vector database
# 3. Searching similar chunks

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config import EMBEDDING_MODEL, TOP_K_RESULTS
import torch


class EmbeddingManager:
    """
    Manages embeddings and vector search using FAISS.
    
    What are embeddings?
    - Convert text into vectors (list of numbers)
    - Similar texts have similar vectors
    - Example: "Python programming" ≈ [0.2, 0.5, -0.3, 0.1, ...]
    """
    
    def __init__(self):
        """Initialize the embedding model."""
        # Auto-detect device (GPU if available, else CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✓ Using device: {self.device.upper()}")
        
        # Load pre-trained sentence transformer model
        self.model = SentenceTransformer(EMBEDDING_MODEL, device=self.device)
        
        # Dimension of embeddings (for all-MiniLM-L6-v2: 384)
        self.embedding_dim = 384
        
        # FAISS index (will be created when embeddings are added)
        self.faiss_index = None
        self.chunks = None
        
        print(f"✓ Model loaded: {EMBEDDING_MODEL}")
        print(f"  - Embedding dimension: {self.embedding_dim}")
    
    def create_embeddings(self, chunks: list):
        """
        Convert text chunks into embeddings.
        
        Args:
            chunks: List of text chunks from loader
            
        Returns:
            Numpy array of embeddings
        """
        print(f"\n🔄 Creating embeddings for {len(chunks)} chunks...")
        
        # Extract text from chunk objects
        texts = [chunk.page_content for chunk in chunks]
        
        # Generate embeddings (returns numpy array)
        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        
        print(f"✓ Generated {len(embeddings)} embeddings")
        print(f"  - Shape: {embeddings.shape}")
        
        return embeddings
    
    def build_faiss_index(self, chunks: list):
        """
        Build FAISS index for fast similarity search.
        
        FAISS = Facebook AI Similarity Search
        Why FAISS?
        - Search 1M vectors in milliseconds
        - Memory efficient
        - No cloud required
        
        Args:
            chunks: List of text chunks
        """
        # Store chunks for later retrieval
        self.chunks = chunks
        
        # Create embeddings
        embeddings = self.create_embeddings(chunks)
        embeddings = embeddings.astype('float32')
        
        # Create FAISS index
        self.faiss_index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Add embeddings to index
        self.faiss_index.add(embeddings)
        
        print(f"✓ FAISS index built successfully")
        print(f"  - Total vectors: {self.faiss_index.ntotal}")
        print(f"  - Ready for search!")
    
    def search_similar_chunks(self, query: str, k: int = TOP_K_RESULTS):
        """
        Find most similar chunks to a query.
        
        Args:
            query: User's question
            k: Number of chunks to retrieve (default: 3)
            
        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        if self.faiss_index is None:
            raise ValueError("FAISS index not built. Call build_faiss_index first.")
        
        # Convert query to embedding (same as chunks)
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        query_embedding = query_embedding.astype('float32')
        
        # Search in FAISS
        distances, indices = self.faiss_index.search(query_embedding, k)
        
        # Retrieve actual chunks
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            chunk_text = self.chunks[idx].page_content
            # Convert distance to similarity score (0-1)
            similarity = 1 / (1 + distance)
            results.append({
                'text': chunk_text,
                'similarity': float(similarity),
                'index': int(idx)
            })
        
        return results
    
    def save_index(self, path: str):
        """Save FAISS index to disk."""
        if self.faiss_index:
            faiss.write_index(self.faiss_index, path)
            print(f"✓ Index saved to {path}")
    
    def load_index(self, path: str):
        """Load FAISS index from disk."""
        self.faiss_index = faiss.read_index(path)
        print(f"✓ Index loaded from {path}")
