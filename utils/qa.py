# ============================================
# QA.PY - Question Answering with RAG
# ============================================
# This module handles:
# 1. Building the RAG pipeline
# 2. Retrieving relevant resume chunks
# 3. Generating answers using LLM

from transformers import pipeline
from config import LLM_MODEL, TOP_K_RESULTS
import torch


class RAG_Pipeline:
    """
    Retrieval-Augmented Generation (RAG) for QA.
    
    How RAG works:
    1. User asks a question
    2. Retrieve most relevant resume chunks
    3. Give chunks to LLM as context
    4. LLM generates answer based on context only
    5. No hallucination - answer strictly from resume
    """
    
    def __init__(self, embedding_manager):
        """
        Initialize RAG pipeline.
        
        Args:
            embedding_manager: Instance of EmbeddingManager class
        """
        self.embedding_manager = embedding_manager
        
        # Auto-detect device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load LLM (Google's FLAN-T5)
        print(f"\n🔄 Loading LLM: {LLM_MODEL}...")
        self.qa_pipeline = pipeline(
            "text2text-generation",
            model=LLM_MODEL,
            device=0 if self.device == "cuda" else -1,
            max_length=512
        )
        print(f"✓ LLM loaded successfully")
    
    def retrieve_context(self, query: str, top_k: int = TOP_K_RESULTS):
        """
        Retrieve relevant resume chunks for the query.
        
        Args:
            query: User's question
            top_k: Number of chunks to retrieve
            
        Returns:
            String of concatenated relevant chunks
        """
        # Search for similar chunks
        results = self.embedding_manager.search_similar_chunks(query, k=top_k)
        
        # Combine chunks into context
        context = "\n\n".join([
            f"[Chunk {i+1}] {result['text']}"
            for i, result in enumerate(results)
        ])
        
        return context, results
    
    def generate_answer(self, query: str, context: str):
        """
        Generate answer using LLM based on retrieved context.
        
        Args:
            query: User's question
            context: Retrieved resume chunks
            
        Returns:
            Generated answer
        """
        # Create the prompt for LLM
        prompt = f"""
Based on the following resume context, answer this question:

QUESTION: {query}

RESUME CONTEXT:
{context}

ANSWER:
"""
        
        # Generate answer
        answer = self.qa_pipeline(
            prompt,
            max_length=512,
            num_beams=1,
            do_sample=False
        )
        
        return answer[0]['generated_text'].strip()
    
    def answer_question(self, query: str, top_k: int = TOP_K_RESULTS):
        """
        Complete RAG pipeline: Retrieve + Generate.
        
        Args:
            query: User's question
            top_k: Number of chunks to retrieve
            
        Returns:
            Dict with answer and source chunks
        """
        # Step 1: Retrieve relevant chunks
        context, sources = self.retrieve_context(query, top_k=top_k)
        
        # Step 2: Generate answer from context
        answer = self.generate_answer(query, context)
        
        return {
            'answer': answer,
            'sources': sources,
            'context': context
        }


def format_answer_with_sources(result: dict) -> str:
    """
    Format RAG result nicely for display.
    
    Args:
        result: Output from RAG pipeline
        
    Returns:
        Formatted string
    """
    output = "📝 **Answer:**\n"
    output += result['answer'] + "\n\n"
    
    output += "📚 **Sources (Confidence Score):**\n"
    for i, source in enumerate(result['sources'], 1):
        confidence = f"{source['similarity']*100:.1f}%"
        output += f"\n{i}. **Relevance: {confidence}**\n"
        output += f"   {source['text'][:200]}...\n"
    
    return output
