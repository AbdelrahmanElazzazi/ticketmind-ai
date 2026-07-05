# ==========================
# Retrieval Configuration
# ==========================

# Minimum similarity score required
CONFIDENCE_THRESHOLD = 0.65
TOP_K = 3

# ==================
# Human Review
# ================

# Tickets above this score are automatically approved
AUTO_APPROVE_THRESHOLD = 0.70

# Tickets below auto approval but above this threshold require human review
HUMAN_REVIEW_THRESHOLD = 0.60

# ==========================
# Model Configuration
# ==========================
EMBEDDING_MODEL = "gemini-embedding-2"
LLM_MODEL = "gemini-2.5-flash"

# ==========================
# Pinecone Configuration
# ==========================
INDEX_NAME = "resolve-ticket-kb"
