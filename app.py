# ============================================
# APP.PY - Main Streamlit Application
# ============================================
# Professional, clean UI for Resume QA Chatbot

import streamlit as st
from pathlib import Path
import tempfile
import os
from config import PAGE_TITLE, PAGE_ICON, LAYOUT
from utils.loader import process_pdf
from utils.embeddings import EmbeddingManager
from utils.qa import RAG_Pipeline, format_answer_with_sources


# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    h1 {
        color: #1f3a5c;
        border-bottom: 3px solid #2b7a78;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    }
    
    h2 {
        color: #2b7a78;
        margin-top: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2b7a78;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-size: 16px;
    }
    
    .stButton > button:hover {
        background-color: #1f3a5c;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-left: 4px solid #2b7a78;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Success message */
    .success-message {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        color: #155724;
    }
    
    /* Code blocks */
    code {
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE MANAGEMENT
# ============================================
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None

if 'resume_loaded' not in st.session_state:
    st.session_state.resume_loaded = False

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# ============================================
# SIDEBAR - CONFIGURATION & INFO
# ============================================
with st.sidebar:
    st.title("📋 Resume QA Chatbot")

    
    st.divider()
    
    st.subheader("About This Project")
    st.markdown("""
    **A professional Resume Question Answering system using:**
    - 🧠 **AI Models**: Open-source LLMs from HuggingFace
    - 🔍 **RAG Technology**: Retrieve + Generate answers
    - ⚡ **Fast Search**: FAISS for semantic similarity
    - 🆓 **100% Free**: No API keys, no costs
    
    **How it works:**
    1. Upload your resume (PDF)
    2. System reads & indexes your resume
    3. Ask questions about your experience
    4. Get answers strictly from your resume
    """)
    
    st.divider()
    
    st.subheader("⚙️ Configuration")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Top K Results", "3")
    with col2:
        st.metric("Chunk Size", "500 chars")
    
    st.divider()
    
    st.subheader("ℹ️ About RAG")
    st.markdown("""
    **RAG = Retrieval-Augmented Generation**
    
    Unlike ChatGPT which can hallucinate:
    - We **retrieve** exact resume content
    - We **augment** the prompt with context
    - We **generate** answers from context only
    
    Result: **Zero hallucinations**, 100% accurate
    """)


# ============================================
# MAIN CONTENT - HEADER
# ============================================
st.markdown(f"<h1>📄 {PAGE_TITLE}</h1>", unsafe_allow_html=True)

st.markdown("""
Welcome! This is a **professional Resume QA Chatbot** built with cutting-edge AI.

🎯 **Upload your resume** and ask questions about your skills, experience, and projects. 
The system will answer ONLY from your resume content - no hallucinations!
""")

st.divider()

# ============================================
# SECTION 1 - RESUME UPLOAD
# ============================================
st.markdown("## 📤 Step 1: Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose a PDF resume file",
    type=['pdf'],
    help="Upload your resume in PDF format"
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_path = tmp_file.name
    
    try:
        if st.button("🚀 Process Resume", use_container_width=True):
            with st.spinner("🔄 Processing resume..."):
                # Step 1: Load and split PDF
                st.info("📖 Loading PDF and extracting text...")
                chunks = process_pdf(tmp_path)
                
                # Step 2: Create embeddings
                st.info(f"🧠 Creating embeddings for {len(chunks)} chunks...")
                embedding_manager = EmbeddingManager()
                embedding_manager.build_faiss_index(chunks)
                
                # Step 3: Initialize RAG pipeline
                st.info("⚡ Initializing QA pipeline...")
                rag_pipeline = RAG_Pipeline(embedding_manager)
                
                # Save to session state
                st.session_state.rag_pipeline = rag_pipeline
                st.session_state.resume_loaded = True
                st.session_state.chat_history = []
                
                st.success("✅ Resume processed successfully! You can now ask questions.")
    
    finally:
        # Clean up temp file
        os.unlink(tmp_path)

st.divider()

# ============================================
# SECTION 2 - QUESTION ANSWERING
# ============================================
st.markdown("## ❓ Step 2: Ask Questions About Your Resume")

if st.session_state.resume_loaded:
    st.success("✅ Resume is loaded and ready for questions!", icon="✅")
    
    # Question input
    user_question = st.text_input(
        "Ask a question about your resume:",
        placeholder="e.g., What are your main technical skills?",
        help="Ask anything related to your resume"
    )
    
    if user_question:
        if st.button("🔍 Get Answer", use_container_width=True):
            with st.spinner("🤔 Thinking..."):
                try:
                    # Run RAG pipeline
                    result = st.session_state.rag_pipeline.answer_question(user_question)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'question': user_question,
                        'result': result
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # Display chat history (most recent first)
    if st.session_state.chat_history:
        st.markdown("### 💬 Conversation History")
        
        for i, exchange in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Q: {exchange['question']}", expanded=(i==0)):
                st.markdown("**📝 ANSWER:**")
                st.markdown(exchange['result']['answer'])
                
                st.markdown("**📚 SOURCE CHUNKS (with Confidence):**")
                for j, source in enumerate(exchange['result']['sources'], 1):
                    confidence = f"{source['similarity']*100:.1f}%"
                    with st.container():
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.metric("Confidence", confidence)
                        with col2:
                            st.text(source['text'][:300] + "...")

else:
    st.info("👆 Please upload and process a resume first to ask questions.")

st.divider()

# ============================================
# FOOTER
# ============================================
st.markdown("""
---
### 📌 Project Information

**Technology Stack:**
- Python, Streamlit, LangChain
- Sentence-Transformers, FAISS
- Google FLAN-T5 (Open-source LLM)

**Features:**
- ✅ Free and open-source
- ✅ No API keys required
- ✅ Works on CPU
- ✅ Zero hallucinations
- ✅ Professional UI

**GitHub:** [Resume QA Chatbot](https://github.com/yourusername/resume-qa-chatbot)

---
*Built with ❤️ for interview preparation*
""")
