Resume QA Chatbot – Professional Guide
🎯 Project Overview
A professional Resume Question Answering Chatbot built with free, open‑source technologies. This project demonstrates Retrieval‑Augmented Generation (RAG) – a practical way to build AI systems that avoid hallucinations by always grounding answers in the resume content.

Perfect for:

Interview preparation

Demonstrating RAG architecture

Portfolio / GitHub projects

Understanding modern AI systems end‑to‑end

📊 Architecture Overview
text
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                       │
│                     (Streamlit Web App)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ┌────────┐   ┌─────────┐   ┌──────────┐
    │  PDF   │   │ Embedder│   │ Question │
    │ Upload │   │(Sentence│   │  Input   │
    │        │   │Transf.) │   │          │
    └────────┘   └─────────┘   └──────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │  FAISS Vector Index  │
            │   (Fast Search DB)   │
            └──────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │   Retrieve Top 3     │
            │   Similar Chunks     │
            └──────────────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │     FLAN‑T5 LLM      │
            │     (Open‑source)    │
            └──────────────────────┘
                       │
                       ▼
                ┌─────────────┐
                │   ANSWER    │
                └─────────────┘
🚀 Quick Start
Prerequisites
Python 3.8 or higher

pip (Python package manager)

4 GB RAM minimum (8 GB recommended)

Internet connection for the first model download

Installation
bash
# 1. Clone or download the project
cd resume_qa_chatbot

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
streamlit run app.py
The app will open at: http://localhost:8501

📝 How to Use
Step 1 – Upload Resume
Click “📤 Step 1: Upload Your Resume”

Select your resume PDF file

Click “🚀 Process Resume”

Wait for processing (first time 1–2 minutes because models load and embed the resume)

Step 2 – Ask Questions
Type a question in the text box

Click “🔍 Get Answer”

Read the answer and inspect the source chunks used

Example questions:

text
What are my main technical skills?
What programming languages do I know?
Describe my experience with Python.
What projects have I worked on?
When did I graduate?
Which companies have I worked at?
🔧 Technical Explanation
What is RAG (Retrieval‑Augmented Generation)?
Problem: A generic LLM (e.g. ChatGPT) can hallucinate – it may invent skills or experience not present in the resume.

Solution: RAG forces the model to answer only from retrieved resume text.

Retrieval – Convert resume into chunks and use semantic search to find the most relevant chunks for a question.

Augmentation – Add these retrieved chunks as explicit context in the prompt.

Generation – The LLM generates an answer using only the provided context.

This ensures the answer stays faithful to the resume.

Main Components
1. PDF Loader (utils/loader.py)
text
Resume PDF
   ↓
PyPDFLoader (extract text)
   ↓
RecursiveCharacterTextSplitter
   ↓
Text chunks (~500 characters each)
   ↓
Ready for embeddings
2. Embedding Manager (utils/embeddings.py)
text
Text chunks
   ↓
Sentence‑Transformers (all‑MiniLM‑L6‑v2)
   ↓
384‑dimensional embeddings
   ↓
FAISS index (fast vector database)
FAISS allows fast similarity search to find the most relevant chunks for a question.

3. QA Pipeline (utils/qa.py)
text
User question
   ↓
Encode question → embedding
   ↓
Search FAISS for nearest chunks
   ↓
Take top‑k (e.g. 3) chunks as context
   ↓
Construct prompt for FLAN‑T5 LLM
   ↓
LLM generates answer from that context
🤖 Models Used
Sentence‑Transformers – all‑MiniLM‑L6‑v2

~22 MB, very small and CPU‑friendly

Good semantic similarity performance

Outputs 384‑dimensional vectors

FLAN‑T5‑base

~250 MB

Instruction‑tuned encoder‑decoder model from Google

Good at following prompts and generating concise answers

FAISS (CPU)

High‑performance similarity search library

Searches thousands of embeddings in milliseconds

All components are completely open‑source and free.
