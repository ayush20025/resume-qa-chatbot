# Configuration file for Resume QA Chatbot
# All settings in one place for easy modification

# ============================================
# MODEL CONFIGURATION
# ============================================
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Why this model?
# - Lightweight (22MB, perfect for CPU)
# - Fast inference
# - Good semantic understanding
# - Works completely offline

LLM_MODEL = "google/flan-t5-base"
# Why this model?
# - Free and open-source
# - Instruction-following capability
# - Fast on CPU (~250MB)
# - Good for Q&A tasks

# ============================================
# TEXT PROCESSING
# ============================================
CHUNK_SIZE = 500
# Split resume into chunks of ~500 characters
# Larger chunks = more context, slower search
# Smaller chunks = precise but may lose context

CHUNK_OVERLAP = 50
# Overlap between consecutive chunks
# Ensures no information is lost at boundaries

# ============================================
# VECTOR SEARCH
# ============================================
TOP_K_RESULTS = 3
# Number of most similar chunks to retrieve
# More = more context but might include irrelevant info
# Less = faster but might miss relevant context

# ============================================
# UI CONFIGURATION
# ============================================
PAGE_TITLE = "Resume QA Chatbot"
PAGE_ICON = "📄"
LAYOUT = "wide"

# ============================================
# MODEL DEVICE (Auto-detected)
# ============================================
# The application will automatically use:
# - GPU if available
# - CPU if GPU not available
# No need to change this manually
